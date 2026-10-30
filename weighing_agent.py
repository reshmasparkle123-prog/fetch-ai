"""
RationSeva Weighing Agent (port 8005) - internal agent, called by the Coordinator.

With a photo: uploads it to the backend POST /scale-check, which stores a
time-stamped proof in Cloudinary, reads the scale display with Cloudinary OCR
and returns OK / SHORT_WEIGHT / NEEDS_REVIEW / UNREADABLE.
Without a photo: compares the weight the user typed with the entitlement.

For SHORT_WEIGHT it returns a complaint DRAFT for the user to review. It never
files anything itself.
"""

import asyncio
import base64
from datetime import date

import requests
from uagents import Context

import ration_data as rd
from common import BackendError, backend_post, make_agent, warm_backend
from messages import WeighingRequest, WeighingResponse

MAX_IMAGE_BYTES = 10 * 1024 * 1024   # backend limit
TOLERANCE_KG = 0.1

agent = make_agent("ration_seva_weighing_agent", "WEIGHING_AGENT_SEED", 8005, "WEIGHING_AGENT_MAILBOX")


def download_image(url):
    if not url.lower().startswith(("http://", "https://")):
        raise ValueError("photo URL must be http(s)")
    with requests.get(url, timeout=20, stream=True) as r:
        r.raise_for_status()
        data = r.raw.read(MAX_IMAGE_BYTES + 1, decode_content=True)
        mime = r.headers.get("Content-Type", "").split(";")[0].strip()
    if len(data) > MAX_IMAGE_BYTES:
        raise ValueError("photo larger than 10 MB")
    return data, mime


def guess_mime(data, hint):
    if hint and hint.startswith("image/"):
        return hint
    if data.startswith(b"\x89PNG"):
        return "image/png"
    if data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "image/webp"
    return "image/jpeg"


def manual_verdict(reading, expected):
    """Same order as the backend's scale_verdict, for a weight the user typed."""
    if reading is None or reading <= 0:
        return "UNREADABLE"
    if reading > expected * 1.5 and reading > expected + 2:
        return "NEEDS_REVIEW"
    if reading + TOLERANCE_KG < expected:
        return "SHORT_WEIGHT"
    return "OK"


COMPLAINT = {
    "en": ("COMPLAINT DRAFT (not sent)\n"
           "To: Civil Supplies Department, Andhra Pradesh (PDS helpline 1967)\n"
           "Subject: Short weight at fair price shop {fps}\n\n"
           "On {day}, at fair price shop {fps} ({afso}, {district}), I received {item} weighing "
           "{reading} kg against my entitlement of {expected} kg - short by {short} kg.\n"
           "{evidence}\n"
           "I request an inspection of the shop's weighing scale and the balance quantity.\n"
           "Name: ______  Ration card no.: ______  Phone: ______"),
    "te": ("ఫిర్యాదు ముసాయిదా (పంపబడలేదు)\n"
           "కు: పౌర సరఫరాల శాఖ, ఆంధ్రప్రదేశ్ (PDS హెల్ప్‌లైన్ 1967)\n"
           "విషయం: రేషన్ షాప్ {fps} లో తక్కువ తూకం\n\n"
           "{day} న, రేషన్ షాప్ {fps} ({afso}, {district}) లో నాకు {expected} కిలోలు రావాల్సి ఉండగా "
           "{item} {reading} కిలోలు మాత్రమే ఇచ్చారు - {short} కిలోలు తక్కువ.\n"
           "{evidence}\n"
           "దయచేసి షాప్ తూకం యంత్రాన్ని తనిఖీ చేసి, మిగిలిన సరుకు ఇప్పించగలరు.\n"
           "పేరు: ______  రేషన్ కార్డు నం.: ______  ఫోన్: ______"),
    "hi": ("शिकायत का मसौदा (भेजा नहीं गया)\n"
           "सेवा में: नागरिक आपूर्ति विभाग, आंध्र प्रदेश (PDS हेल्पलाइन 1967)\n"
           "विषय: राशन दुकान {fps} पर कम तौल\n\n"
           "{day} को राशन दुकान {fps} ({afso}, {district}) पर मुझे {expected} किलो के हक़ के बदले "
           "{item} केवल {reading} किलो मिला - {short} किलो कम।\n"
           "{evidence}\n"
           "कृपया दुकान के तराज़ू की जाँच करें और बाकी राशन दिलवाएँ।\n"
           "नाम: ______  राशन कार्ड नं.: ______  फ़ोन: ______"),
}

EVIDENCE = {
    "en": ("Photo proof (time-stamped, stored by RationSeva on Cloudinary): {url}", "Weight as reported by me (no photo)."),
    "te": ("ఫోటో రుజువు (సమయ ముద్రతో, Cloudinary లో భద్రపరచబడింది): {url}", "బరువు నేను స్వయంగా తెలిపినది (ఫోటో లేదు)."),
    "hi": ("फोटो सबूत (समय की मुहर सहित, Cloudinary पर सुरक्षित): {url}", "वज़न मेरे द्वारा बताया गया (फोटो नहीं)।"),
}


def complaint_draft(lang, fps_id, commodity, reading, expected, proof_url):
    lang = lang if lang in COMPLAINT else "en"
    shop = rd.find_shop(fps_id) or {}
    with_photo, without = EVIDENCE[lang]
    item = rd.display_name(rd.dataset_names(commodity)[0], lang) if rd.dataset_names(commodity) else \
        {"en": "ration", "te": "రేషన్", "hi": "राशन"}[lang]
    return COMPLAINT[lang].format(
        fps=fps_id, afso=shop.get("afso", "-"), district=shop.get("district", "-"),
        day=date.today().isoformat(), item=item, reading=f"{reading:g}", expected=f"{expected:g}",
        short=f"{expected - reading:.2f}",
        evidence=with_photo.format(url=proof_url) if proof_url else without,
    )


async def check(msg: WeighingRequest, logger) -> WeighingResponse:
    base = dict(fps_id=msg.fps_id, expected_kg=msg.expected_kg)

    if not (msg.image_url or msg.image_b64):
        if msg.reported_kg is None:
            return WeighingResponse(ok=False, error="need a photo or the weight you received", **base)
        verdict = manual_verdict(msg.reported_kg, msg.expected_kg)
        result = {"verdict": verdict, "reading_kg": msg.reported_kg, "stamped_url": None}
    else:
        try:
            if msg.image_b64:
                data, mime = base64.b64decode(msg.image_b64), msg.image_mime
            else:
                data, mime = await asyncio.to_thread(download_image, msg.image_url)
        except (ValueError, requests.RequestException) as e:
            return WeighingResponse(ok=False, error=f"could not get the photo: {e}", **base)
        mime = guess_mime(data, mime)
        form = {"fps_id": msg.fps_id, "expected_kg": str(msg.expected_kg), "tolerance_kg": str(TOLERANCE_KG)}
        if msg.commodity:
            form["commodity"] = msg.commodity
        try:
            result = await backend_post("/scale-check", form,
                                        files={"image": (f"scale.{mime.split('/')[1]}", data, mime)})
        except BackendError as e:
            logger.warning(f"/scale-check failed: {e} (status={e.status}, retryable={e.retryable})")
            return WeighingResponse(ok=False, error=str(e), retryable=e.retryable, **base)

    verdict, reading = result["verdict"], result.get("reading_kg")
    short = round(msg.expected_kg - reading, 2) if verdict == "SHORT_WEIGHT" else None
    proof_url = result.get("stamped_url")
    return WeighingResponse(
        ok=True, verdict=verdict, reading_kg=reading, short_by_kg=short,
        message=result.get("message") or verdict, proof_url=proof_url,
        ocr_used=bool(msg.image_url or msg.image_b64),
        complaint_draft=(complaint_draft(msg.language, msg.fps_id, msg.commodity, reading, msg.expected_kg, proof_url)
                         if verdict == "SHORT_WEIGHT" else None),
        **base,
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    await warm_backend(ctx.logger)


@agent.on_message(model=WeighingRequest, replies={WeighingResponse})
async def handle_weighing_request(ctx: Context, sender: str, msg: WeighingRequest):
    ctx.logger.info(f"Weighing request fps_id={msg.fps_id} expected={msg.expected_kg} "
                    f"photo={'url' if msg.image_url else 'bytes' if msg.image_b64 else 'none'} "
                    f"reported={msg.reported_kg}")
    response = await check(msg, ctx.logger)
    ctx.logger.info(f"-> ok={response.ok} verdict={response.verdict} reading={response.reading_kg} "
                    f"error={response.error}")
    await ctx.send(sender, response)


if __name__ == "__main__":
    agent.run()
