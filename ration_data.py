"""
Shared access to the RationSeva stock snapshot (data/summary.json).

The file is a dated snapshot of the AP AePDS "Date wise Stock Details" public
report (480 fair-price shops, Alluri Sitharama Raju district). It is NOT live.
Nothing in this module invents data: unknown shops / commodities return None or [].
"""

import json
import os
import re
from functools import lru_cache

DATA_PATH = os.getenv(
    "RATION_DATA_PATH",
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "summary.json"),
)

# Same thresholds as the ingest script that produced summary.json.
LOW_STOCK_RATIO = 0.10    # closing < 10% of this month's available stock => LOW
OUT_EPSILON = 0.01        # closing <= 0.01 => OUT_OF_STOCK

# Empty sacks the shop returns ("10KG BAG", "15KG BAG", gunny bags) - not ration.
PACKAGING_RE = re.compile(r"\bbags?\b|gunny", re.I)

# commodity key -> (dataset names, words users type in en / te / hi)
COMMODITIES = {
    "rice": (["Rice"], ["rice", "biyyam", "chawal", "బియ్యం", "चावल"]),
    "sugar": (["Sugar", "SUGAR HALF KG"], ["sugar", "chakkera", "cheeni", "చక్కెర", "పంచదార", "चीनी", "शक्कर"]),
    "ragi": (["Raagi", "RagiPowder 1kg"], ["ragi", "raagi", "రాగి", "రాగులు", "रागी"]),
    "atta": (["WM Atta Pkt"], ["atta", "wheat", "గోధుమ", "आटा", "गेहूं", "गेहूँ"]),
    "dal": (["RG Dal One kg Pkt", "Redgram Dal", "Flood Dal"],
            ["dal", "dhal", "pappu", "redgram", "toor", "పప్పు", "కంది", "दाल", "अरहर"]),
    "oil": (["Flood Poil"], ["oil", "palm oil", "నూనె", "तेल"]),
}

DISPLAY_NAMES = {
    "Rice": {"en": "Rice", "te": "బియ్యం", "hi": "चावल"},
    "Sugar": {"en": "Sugar", "te": "చక్కెర", "hi": "चीनी"},
    "SUGAR HALF KG": {"en": "Sugar (½ kg pkt)", "te": "చక్కెర (అర కిలో ప్యాకెట్)", "hi": "चीनी (आधा किलो पैकेट)"},
    "Raagi": {"en": "Ragi", "te": "రాగులు", "hi": "रागी"},
    "RagiPowder 1kg": {"en": "Ragi powder (1 kg pkt)", "te": "రాగి పిండి (1 కిలో ప్యాకెట్)", "hi": "रागी आटा (1 किलो पैकेट)"},
    "WM Atta Pkt": {"en": "Wheat atta (pkt)", "te": "గోధుమ పిండి (ప్యాకెట్)", "hi": "गेहूं का आटा (पैकेट)"},
    "RG Dal One kg Pkt": {"en": "Red gram dal (1 kg pkt)", "te": "కందిపప్పు (1 కిలో ప్యాకెట్)", "hi": "अरहर दाल (1 किलो पैकेट)"},
    "Redgram Dal": {"en": "Red gram dal", "te": "కందిపప్పు", "hi": "अरहर दाल"},
    "Flood Dal": {"en": "Dal (flood relief)", "te": "పప్పు (వరద సహాయం)", "hi": "दाल (बाढ़ राहत)"},
    "Flood Poil": {"en": "Palm oil (flood relief)", "te": "పామాయిల్ (వరద సహాయం)", "hi": "पाम तेल (बाढ़ राहत)"},
}


@lru_cache(maxsize=1)
def load_shops():
    """fps_id -> shop record. Raises if the file is missing or obviously truncated."""
    with open(DATA_PATH, encoding="utf-8") as f:
        records = json.load(f)
    if not isinstance(records, list) or len(records) < 2:
        raise RuntimeError(f"{DATA_PATH} looks incomplete ({len(records) if isinstance(records, list) else 'not a list'} records)")
    return {str(r["fps_id"]): r for r in records}


def find_shop(fps_id):
    return load_shops().get(str(fps_id).strip())


def shop_count():
    return len(load_shops())


def data_time():
    return next(iter(load_shops().values())).get("data_time")


def is_packaging(name):
    return bool(PACKAGING_RE.search(name))


def commodity_key(name_or_word):
    """Map a dataset name or a user word to a commodity key ('rice', 'sugar', ...)."""
    if not name_or_word:
        return None
    w = name_or_word.strip().lower()
    for key, (names, words) in COMMODITIES.items():
        if w == key or w in (n.lower() for n in names) or w in words:
            return key
    return None


def find_commodity_in_text(text):
    """First commodity key mentioned in free text (en / te / hi), else None."""
    low = text.lower()
    hits = []
    for key, (_, words) in COMMODITIES.items():
        for w in words:
            pattern = rf"\b{re.escape(w)}\b" if w.isascii() else re.escape(w)
            m = re.search(pattern, low)
            if m:
                hits.append((m.start(), key))
    return min(hits)[1] if hits else None


def dataset_names(key):
    return COMMODITIES[key][0] if key in COMMODITIES else []


def display_name(name, lang="en"):
    return DISPLAY_NAMES.get(name, {}).get(lang) or DISPLAY_NAMES.get(name, {}).get("en") or name


def classify(closing, issued):
    """Status from quantities: month's available stock = opening + received = closing + issued."""
    available = closing + issued
    if closing <= OUT_EPSILON:
        return "OUT_OF_STOCK"
    if available > 0 and closing / available < LOW_STOCK_RATIO:
        return "LOW"
    return "AVAILABLE"


def ration_items(shop, key=None):
    """The shop's commodities (packaging excluded), optionally filtered to one commodity key."""
    items = [c for c in shop["commodities"] if not is_packaging(c["commodity"])]
    if key:
        names = set(dataset_names(key))
        items = [c for c in items if c["commodity"] in names]
    return items


def alternatives(fps_id, commodity_name, limit=3):
    """Other shops in the same AFSO with `commodity_name` AVAILABLE, most stock first."""
    shop = find_shop(fps_id)
    if not shop:
        return []
    found = []
    for other in load_shops().values():
        if other["fps_id"] == shop["fps_id"] or other["afso"] != shop["afso"]:
            continue
        for c in other["commodities"]:
            if c["commodity"] == commodity_name and classify(c["closing"], c["issued"]) == "AVAILABLE":
                found.append((other, c))
    found.sort(key=lambda oc: oc[1]["closing"], reverse=True)
    return found[:limit]
