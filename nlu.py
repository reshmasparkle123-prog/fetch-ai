"""
Rule-based understanding of free text in English / Telugu / Hindi for the Coordinator.

Deliberately keyword-based (no LLM): predictable, testable, and it never makes up
a shop number or a quantity - anything missing becomes a follow-up question.
"""

import re
from dataclasses import dataclass
from typing import Optional

from ration_data import find_commodity_in_text

TELUGU = re.compile(r"[ఀ-౿]")
DEVANAGARI = re.compile(r"[ऀ-ॿ]")
# Telugu and Devanagari digits -> ASCII
DIGITS = str.maketrans("౦౧౨౩౪౫౬౭౮౯०१२३४५६७८९", "01234567890123456789")

# Checked in this order: "check my ration weight" is weighing, "Telugu stock notice" is notice.
INTENT_WORDS = [
    ("weighing", ["weigh", "weight", "scale", "తూకం", "తూకము", "బరువు", "తక్కువ తూక", "तौल", "तोल", "वजन",
                  "वज़न", "तराजू", "तराज़ू"]),
    ("notice", ["notice", "poster", "flyer", "నోటీసు", "నోటీస్", "పోస్టర్", "नोटिस", "पोस्टर", "सूचना"]),
    ("alternatives", ["where else", "other shop", "another shop", "alternative", "nearby", "near by",
                      "other fps", "elsewhere", "ఇంకెక్కడ", "ఇంకా ఎక్కడ", "వేరే షాప", "వేరే దుకాణ", "ఇతర షాప",
                      "ఎక్కడ దొరుకు", "दूसरी दुकान", "और कहाँ", "और कहां", "कहाँ और", "कहां और", "अन्य दुकान",
                      "कहाँ मिलेगा", "कहां मिलेगा"]),
    ("stock", ["stock", "available", "availability", "is there", "do they have", "how much", "check",
               "ఉందా", "ఉన్నాయా", "నిల్వ", "స్టాక్", "అందుబాటు", "उपलब्ध", "स्टॉक", "है क्या", "है?", "मिलेगा"]),
]

NOTICE_LANG = [
    ("te", ["telugu", "తెలుగు", "तेलुगु"]),
    ("hi", ["hindi", "हिंदी", "हिन्दी", "హిందీ"]),
    ("en", ["english", "ఇంగ్లీష్", "ఆంగ్ల", "अंग्रेज़ी", "अंग्रेजी", "इंग्लिश"]),
]

YES = {"yes", "y", "confirm", "confirmed", "ok", "okay", "sure", "అవును", "సరే", "ఓకే", "हाँ", "हां", "ठीक", "ठीक है",
       "पक्का"}
NO = {"no", "n", "cancel", "discard", "stop", "వద్దు", "కాదు", "नहीं", "रद्द", "मत भेजो"}

KG_UNIT = r"(?:kgs?|kilo(?:gram)?s?|kilos|కిలో[ఀ-౿]*|కేజీ[ఀ-౿]*|किलो|केजी|कि\.?ग्रा\.?)"
KG_RE = re.compile(rf"(?<![\d.])(\d{{1,3}}(?:\.\d+)?)\s*{KG_UNIT}", re.I)
BARE_NUMBER_RE = re.compile(r"(?<![\d.])(\d{1,3}(?:\.\d+)?)(?![\d.])")
FPS_RE = re.compile(r"(?<!\d)(\d{7})(?!\d)")

# Words that mark a kg number as the ENTITLEMENT. English puts them before the number
# ("instead of 20 kg"), Telugu / Hindi after it ("20 కిలోలు రావాలి", "20 किलो मिलना चाहिए").
EXPECTED_BEFORE = re.compile(r"(instead of|out of|entitled|entitlement|should (?:be|get|have got)|supposed to"
                             r"|expected|eligible|quota|అర్హత|हक़|हक)\W*(?:to|is|of|for)?\W*$", re.I)
EXPECTED_AFTER = re.compile(r"^\W*(రావాలి|రావాల్సి|ఇవ్వాలి|బదులు|मिलना चाहिए|मिलने चाहिए|चाहिए|के बजाय"
                            r"|के बदले|entitled|expected|due)", re.I)
RECEIVED_WORDS = re.compile(r"\b(got|received|gave|given|only)\b|వచ్చింది|ఇచ్చారు|ఇచ్చాడు|मिला|दिया|दिए", re.I)


@dataclass
class Parsed:
    language: str
    intent: Optional[str]
    fps_id: Optional[str]
    commodity: Optional[str]
    notice_language: Optional[str]
    expected_kg: Optional[float]
    reported_kg: Optional[float]
    bare_number: Optional[float]


def detect_language(text):
    te, hi = len(TELUGU.findall(text)), len(DEVANAGARI.findall(text))
    if te == hi == 0:
        return "en"
    return "te" if te >= hi else "hi"


def _contains(low, words):
    for w in words:
        if (re.search(rf"\b{re.escape(w)}\b", low) if w.isascii() and w[-1].isalnum() else w in low):
            return True
    return False


def detect_intent(low):
    for intent, words in INTENT_WORDS:
        if _contains(low, words):
            return intent
    return None


def detect_notice_language(low):
    for lang, words in NOTICE_LANG:
        if _contains(low, words):
            return lang
    return None


def extract_weights(text, has_photo):
    """(expected_kg, reported_kg) from the kg numbers in the text."""
    matches = list(KG_RE.finditer(text))
    if not matches:
        return None, None
    values, marked = [float(m.group(1)) for m in matches], None
    for i, m in enumerate(matches):
        before = text[matches[i - 1].end() if i else max(0, m.start() - 40):m.start()]
        after = text[m.end():matches[i + 1].start() if i + 1 < len(matches) else m.end() + 40]
        if EXPECTED_BEFORE.search(before) or EXPECTED_AFTER.search(after):
            marked = i
            break

    if len(values) >= 2:
        if marked is None:                       # "18 kg ... 20 kg": assume a short-weight complaint
            return max(values[:2]), min(values[:2])
        other = next(v for j, v in enumerate(values) if j != marked)
        return values[marked], other
    value = values[0]
    if marked is not None or has_photo or not RECEIVED_WORDS.search(text):
        return value, None
    return None, value


def is_yes(text):
    return text.strip().lower().strip("!. ।") in YES


def is_no(text):
    return text.strip().lower().strip("!. ।") in NO


def parse(text, has_photo=False):
    text = (text or "").translate(DIGITS)
    low = text.lower()
    fps = FPS_RE.search(text)
    without_fps = FPS_RE.sub(" ", text)
    expected, reported = extract_weights(without_fps, has_photo)
    bare = BARE_NUMBER_RE.search(without_fps)
    return Parsed(
        language=detect_language(text),
        intent=detect_intent(low),
        fps_id=fps.group(1) if fps else None,
        commodity=find_commodity_in_text(text),
        notice_language=detect_notice_language(low),
        expected_kg=expected,
        reported_kg=reported,
        bare_number=float(bare.group(1)) if bare else None,
    )
