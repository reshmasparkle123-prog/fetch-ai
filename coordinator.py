"""
RationSeva Coordinator (port 8002) - the ONLY chat-protocol (ASI:One) agent.

Understands free text in English / Telugu / Hindi, extracts the 7-digit FPS id,
commodity, notice language and weights, asks a follow-up when something is
missing, and routes to the internal agents with send_and_receive:

  stock check    -> Stock Validator -> Shortage Analyst
  where else?    -> Stock Validator -> Shortage Analyst (alternatives)
  stock notice   -> Notice Agent    -> backend POST /notice      (Cloudinary)
  weighing check -> Weighing Agent  -> backend POST /scale-check (Cloudinary OCR)

Every agent call has a 30 s timeout and is retried once (an agent restarting,
or the Render backend waking up). If an agent stays down the user gets a clear,
localized "service unavailable" reply - never invented data.
"""

import asyncio
import os
import time
from datetime import datetime, timezone
from uuid import uuid4

import requests
from uagents import Context, Protocol
from uagents_core.config import AgentverseConfig
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    ResourceContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)
from uagents_core.storage import ExternalStorage

import nlu
import replies as R
from common import env_flag, make_agent, require_env
from messages import (
    NoticeRequest, NoticeResponse, ShortageAnalysis, ShortageRequest,
    StockRequest, StockResponse, WeighingRequest, WeighingResponse,
)

STOCK_VALIDATOR_ADDRESS = require_env("STOCK_VALIDATOR_ADDRESS")
SHORTAGE_ANALYST_ADDRESS = require_env("SHORTAGE_ANALYST_ADDRESS")
NOTICE_AGENT_ADDRESS = require_env("NOTICE_AGENT_ADDRESS")
WEIGHING_AGENT_ADDRESS = require_env("WEIGHING_AGENT_ADDRESS")

AGENT_TIMEOUT = int(os.getenv("AGENT_TIMEOUT", "30"))
PENDING_TTL = 30 * 60          # forget an unanswered follow-up after 30 min
MAX_PHOTO_BYTES = 10 * 1024 * 1024

# Mailbox (Agentverse / ASI:One) unless COORDINATOR_MAILBOX=false for local tests.
os.environ.setdefault("COORDINATOR_MAILBOX", "true")
agent = make_agent("ration_seva_coordinator", "RATION_COORDINATOR_SEED", 8002, "COORDINATOR_MAILBOX")
chat_protocol = Protocol(spec=chat_protocol_spec)


# ------------------------------------------------------------ helpers ---

def chat_message(text, end_session):
    content = [TextContent(type="text", text=text)]
    if end_session:
        content.append(EndSessionContent(type="end-session"))
    return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)


async def ask(ctx, address, request, response_type, label):
    """send_and_receive with a 30 s timeout and one retry. Returns the reply or None."""
    reply = None
    for attempt in (1, 2):
        reply, status = await ctx.send_and_receive(address, request, response_type=response_type,
                                                   timeout=AGENT_TIMEOUT)
        if reply is not None and not getattr(reply, "retryable", False):
            return reply
        reason = getattr(reply, "error", None) if reply is not None else f"{status.status}: {status.detail}"
        ctx.logger.warning(f"{label} attempt {attempt} failed ({reason})")
        if attempt == 1:
            await asyncio.sleep(2)
    return reply if reply is not None and getattr(reply, "ok", True) else None


def attachment_ref(msg):
    """First image attachment in an ASI:One message -> a small JSON-safe reference."""
    for item in msg.content:
        if isinstance(item, ResourceContent):
            res = item.resource[0] if isinstance(item.resource, list) else item.resource
            return {"uri": res.uri, "resource_id": str(item.resource_id),
                    "mime": (res.metadata or {}).get("mime_type", "")}
    return None


def fetch_photo(ctx, ref):
    """(image_url, image_b64, mime) for the Weighing Agent.

    Public http(s) URLs are passed through (the Weighing Agent downloads them).
    ASI:One attachments live in Agentverse storage and only THIS agent was granted
    read access, so the Coordinator downloads them and forwards the bytes.
    """
    uri = ref["uri"]
    if uri.startswith(("http://", "https://")):
        return uri, None, ref["mime"] or None
    if uri.startswith("data:"):
        header, _, data = uri.partition(",")
        return None, data, header[5:].split(";")[0] or None
    storage = ExternalStorage(identity=ctx.agent.identity, storage_url=AgentverseConfig().storage_api)
    asset = storage.download(ref["resource_id"])
    contents = asset["contents"]
    if len(contents) * 3 / 4 > MAX_PHOTO_BYTES:
        raise ValueError("photo larger than 10 MB")
    return None, contents, asset.get("mime_type") or ref["mime"] or None


def load_state(ctx, sender):
    state = ctx.storage.get(f"chat:{sender}") or {}
    if state.get("pending") and time.time() - state["pending"].get("at", 0) > PENDING_TTL:
        state.pop("pending")
    return state


def save_state(ctx, sender, state):
    ctx.storage.set(f"chat:{sender}", state)


# -------------------------------------------------------------- flows ---

async def get_stock(ctx, fps_id, commodity, lang):
    """(StockResponse, None) or (None, error reply text)."""
    stock = await ask(ctx, STOCK_VALIDATOR_ADDRESS, StockRequest(fps_id=fps_id, commodity=commodity),
                      StockResponse, "stock validator")
    if stock is None:
        return None, R.t("service_down", lang, service=R.t("svc_stock", lang))
    if not stock.found:
        return None, R.not_found(fps_id, lang)
    return stock, None


async def get_analysis(ctx, stock, want_alternatives):
    if not stock.commodities:
        return None
    return await ask(ctx, SHORTAGE_ANALYST_ADDRESS,
                     ShortageRequest(fps_id=stock.fps_id, afso=stock.afso, commodities=stock.commodities,
                                     commodity_requested=stock.commodity_requested,
                                     want_alternatives=want_alternatives),
                     ShortageAnalysis, "shortage analyst")


async def stock_flow(ctx, req, lang):
    stock, error = await get_stock(ctx, req["fps_id"], req.get("commodity"), lang)
    if error:
        return error
    return R.stock_reply(stock, await get_analysis(ctx, stock, want_alternatives=False), lang)


async def alternatives_flow(ctx, req, lang):
    stock, error = await get_stock(ctx, req["fps_id"], req.get("commodity"), lang)
    if error:
        return error
    analysis = await get_analysis(ctx, stock, want_alternatives=True)
    if analysis is None:                                # analyst down: still show the real report
        return R.stock_reply(stock, None, lang)
    return R.alternatives_reply(stock, analysis, lang)


async def notice_flow(ctx, req, lang):
    notice_lang = req.get("notice_language") or (lang if lang in ("te", "hi") else "te")
    notice = await ask(ctx, NOTICE_AGENT_ADDRESS, NoticeRequest(fps_id=req["fps_id"], language=notice_lang),
                       NoticeResponse, "notice agent")
    if notice is not None and notice.ok:
        return R.notice_reply(notice, lang)
    stock, error = await get_stock(ctx, req["fps_id"], None, lang)
    if error:                                           # unknown shop (or stock service down too)
        return error
    if notice is not None and notice.not_found:         # known shop but nothing available to print
        return R.t("notice_empty", lang, fps=req["fps_id"])
    return "\n\n".join([R.t("service_down", lang, service=R.t("svc_notice", lang)),
                        R.t("fallback_text", lang),
                        R.stock_reply(stock, await get_analysis(ctx, stock, want_alternatives=False), lang)])


async def weighing_flow(ctx, req, lang):
    """Returns (reply text, complaint draft or None)."""
    image_url = image_b64 = mime = None
    if req.get("image"):
        try:
            image_url, image_b64, mime = await asyncio.to_thread(fetch_photo, ctx, req["image"])
        except (ValueError, RuntimeError, requests.RequestException, KeyError) as e:
            ctx.logger.warning(f"Could not fetch attachment: {e}")
            return R.t("photo_error", lang), None
    request = WeighingRequest(fps_id=req["fps_id"], expected_kg=req["expected_kg"], commodity=req.get("commodity"),
                              image_url=image_url, image_b64=image_b64, image_mime=mime,
                              reported_kg=None if req.get("image") else req.get("reported_kg"), language=lang)
    result = await ask(ctx, WEIGHING_AGENT_ADDRESS, request, WeighingResponse, "weighing agent")
    if result is None:
        return R.t("service_down", lang, service=R.t("svc_weighing", lang)), None
    if not result.ok:
        return R.t("photo_error", lang), None
    return R.weighing_reply(result, lang), result.complaint_draft


def missing_for(req):
    """Which follow-up to ask before this request can be routed."""
    if req["intent"] == "weighing":
        if not req.get("image") and req.get("reported_kg") is None:
            return "photo_or_weight"
        if not req.get("fps_id") or not req.get("expected_kg"):
            return "weigh_details"
    elif not req.get("fps_id"):
        return "fps"
    return None


def follow_up(req, missing, lang):
    if missing == "fps":
        return R.t("ask_fps", lang)
    if missing == "photo_or_weight":
        return R.t("ask_photo_or_weight", lang)
    parts = []
    if not req.get("fps_id"):
        parts.append(R.t("need_fps", lang))
    if not req.get("expected_kg"):
        parts.append(R.t("need_expected", lang))
    prefix = R.t("photo_received", lang) if req.get("image") else ""
    return prefix + R.t("please_tell", lang, x=R.t("and", lang).join(parts))


async def handle(ctx, sender, text, photo):
    """Returns (reply, end_session)."""
    state = load_state(ctx, sender)
    lang = nlu.detect_language(text) if text.strip() else state.get("lang", "en")
    state["lang"] = lang

    # 1. Waiting for the user to confirm / cancel a complaint draft.
    draft = state.pop("complaint", None)
    if draft and not photo:
        if nlu.is_yes(text):
            save_state(ctx, sender, state)
            final = draft.split("\n", 1)[1].lstrip() if "\n" in draft else draft
            return "\n".join([R.t("confirmed", lang), "", "```", final, "```"]), True
        if nlu.is_no(text):
            save_state(ctx, sender, state)
            return R.t("cancelled", lang), True

    # 2. Merge this message into any pending follow-up.
    pending = state.pop("pending", None) or {}
    p = nlu.parse(text, has_photo=bool(photo or pending.get("image")))
    intent = "weighing" if photo else p.intent
    if intent is None and (p.expected_kg or p.reported_kg) and not pending:
        intent = "weighing"
    if intent and pending and intent != pending.get("intent"):
        pending = {}                                     # user changed topic
    intent = intent or pending.get("intent") or ("stock" if p.fps_id else None)
    if intent is None:
        save_state(ctx, sender, state)
        return R.t("welcome", lang), False

    req = {
        "intent": intent,
        "fps_id": p.fps_id or pending.get("fps_id"),
        "commodity": p.commodity or pending.get("commodity"),
        "notice_language": p.notice_language or pending.get("notice_language"),
        "expected_kg": p.expected_kg or pending.get("expected_kg"),
        "reported_kg": p.reported_kg or pending.get("reported_kg"),
        "image": photo or pending.get("image"),
    }
    if intent == "weighing" and not req["expected_kg"] and pending.get("intent") == "weighing" and p.bare_number:
        req["expected_kg"] = p.bare_number               # answer to "how many kg are you entitled to?"

    missing = missing_for(req)
    if missing:
        state["pending"] = {**req, "at": time.time()}
        save_state(ctx, sender, state)
        ctx.logger.info(f"Follow-up '{missing}' for {req}")
        return follow_up(req, missing, lang), False

    ctx.logger.info(f"Routing {intent}: fps={req['fps_id']} commodity={req['commodity']} "
                    f"notice_lang={req['notice_language']} expected={req['expected_kg']} "
                    f"reported={req['reported_kg']} photo={bool(req['image'])}")
    end = True
    if intent == "stock":
        reply = await stock_flow(ctx, req, lang)
    elif intent == "alternatives":
        reply = await alternatives_flow(ctx, req, lang)
    elif intent == "notice":
        reply = await notice_flow(ctx, req, lang)
    else:
        reply, draft = await weighing_flow(ctx, req, lang)
        if draft:
            state["complaint"] = draft                   # wait for explicit confirm - never auto-file
            end = False
    save_state(ctx, sender, state)
    return reply, end


# ------------------------------------------------------- chat protocol ---

@chat_protocol.on_message(ChatMessage)
async def handle_chat_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc),
                                               acknowledged_msg_id=msg.msg_id))
    text = " ".join(item.text for item in msg.content if isinstance(item, TextContent)).strip()
    photo = attachment_ref(msg)
    ctx.logger.info(f"Chat from {sender[:16]}...: {text!r} photo={bool(photo)}")

    if not text and not photo:
        if any(isinstance(item, StartSessionContent) for item in msg.content):
            return                                       # session opened, nothing asked yet
        reply, end = R.t("welcome", "en"), False
    else:
        try:
            reply, end = await handle(ctx, sender, text, photo)
        except Exception:
            ctx.logger.exception("Coordinator failed")
            lang = nlu.detect_language(text)
            reply, end = R.t("service_down", lang, service=R.t("svc_stock", lang)), True

    await ctx.send(sender, chat_message(reply, end))
    ctx.logger.info(f"Replied ({len(reply)} chars, end_session={end})")


@chat_protocol.on_message(ChatAcknowledgement)
async def handle_chat_acknowledgement(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.debug(f"Ack from {sender[:16]}... for {msg.acknowledged_msg_id}")


agent.include(chat_protocol, publish_manifest=True)


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Coordinator address: {agent.address}")
    ctx.logger.info(f"Mailbox: {env_flag('COORDINATOR_MAILBOX')}")


if __name__ == "__main__":
    agent.run()
