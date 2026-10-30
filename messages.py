"""
Structured messages exchanged between the Coordinator and the internal agents.

Only the Coordinator speaks the ASI:One chat protocol; every other agent
handles exactly one request model and replies with one response model.
"""

from typing import Dict, List, Optional

from uagents import Model


# ---------------------------------------------------------------- stock ---

class StockRequest(Model):
    fps_id: str
    commodity: Optional[str] = None   # key like "rice" / "sugar"; None = all items


class CommodityStock(Model):
    commodity: str        # dataset name, e.g. "Rice", "SUGAR HALF KG"
    unit: str             # KG / PKT
    closing: float        # closing balance at data_time
    received: float       # received this month
    issued: float         # issued this month
    available: float      # this month's available stock = closing + issued
    status: str           # AVAILABLE / LOW / OUT_OF_STOCK


class StockFlag(Model):
    commodity: str
    flag: str             # LOW_STOCK / FRACTIONAL_PACKETS / NEGATIVE_VALUE ...
    severity: str
    message: str


class StockResponse(Model):
    found: bool
    fps_id: str
    commodity_requested: Optional[str] = None
    district: Optional[str] = None
    afso: Optional[str] = None
    data_time: Optional[str] = None
    report_date: Optional[str] = None
    source: Optional[str] = None
    is_live: bool = False
    commodities: List[CommodityStock] = []
    flags: List[StockFlag] = []
    message: str = ""


# ------------------------------------------------------------- shortage ---

class ShortageRequest(Model):
    fps_id: str
    afso: str
    commodities: List[CommodityStock]   # from the Stock Validator
    commodity_requested: Optional[str] = None
    want_alternatives: bool = False     # True = user asked "where else can I go?"


class CommodityAssessment(Model):
    commodity: str
    unit: str
    closing: float
    available: float
    percent_left: float
    status: str


class AlternativeShop(Model):
    fps_id: str
    afso: str
    commodity: str
    unit: str
    closing: float
    status: str


class ShortageAnalysis(Model):
    fps_id: str
    afso: str
    assessments: List[CommodityAssessment] = []
    # commodity name -> up to 3 other shops in the same AFSO with it AVAILABLE
    alternatives: Dict[str, List[AlternativeShop]] = {}
    data_time: Optional[str] = None
    analysis: str = ""


# --------------------------------------------------------------- notice ---

class NoticeRequest(Model):
    fps_id: str
    language: str = "te"   # te / hi / en


class NoticeResponse(Model):
    ok: bool
    fps_id: str
    language: str
    url: Optional[str] = None            # Cloudinary-rendered notice image
    items: List[dict] = []               # [{"commodity", "status"}]
    data_time: Optional[str] = None
    error: Optional[str] = None
    not_found: bool = False
    retryable: bool = False              # backend asleep / 5xx -> Coordinator may retry once


# ------------------------------------------------------------- weighing ---

class WeighingRequest(Model):
    fps_id: str
    expected_kg: float
    commodity: Optional[str] = None
    image_url: Optional[str] = None      # public http(s) photo URL - agent downloads it
    image_b64: Optional[str] = None      # or the photo bytes (Coordinator fetched them)
    image_mime: Optional[str] = None
    reported_kg: Optional[float] = None  # no photo: weight typed by the user
    language: str = "en"                 # language of the complaint draft


class WeighingResponse(Model):
    ok: bool
    fps_id: str
    verdict: Optional[str] = None        # OK / SHORT_WEIGHT / NEEDS_REVIEW / UNREADABLE / OCR_UNAVAILABLE
    reading_kg: Optional[float] = None
    expected_kg: float = 0.0
    short_by_kg: Optional[float] = None
    message: str = ""
    proof_url: Optional[str] = None      # Cloudinary stamped proof photo
    ocr_used: bool = False
    complaint_draft: Optional[str] = None
    error: Optional[str] = None
    retryable: bool = False
