
from uagents import Model


class StockRequest(Model):
    commodity: str


class ValidatedStock(Model):
    commodity: str
    opening: float
    received: float
    issued: float
    closing: float
    report_date: str
    validation_passed: bool


class StockResponse(Model):
    report: str
    stock: ValidatedStock


class ShortageAnalysis(Model):
    analysis: str
    illustrative_only: bool = True

