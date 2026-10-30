"""
RationSeva Stock Validator (port 8001)

Looks up a fair-price shop by fps_id (+ optional commodity) in data/summary.json
and returns the real reported quantities, status, data_time, source and flags.
Unknown shops get found=False - nothing is ever fabricated.

Structured messages only (StockRequest -> StockResponse). The ASI:One chat
protocol lives in coordinator.py.
"""

from uagents import Context

import ration_data as rd
from common import make_agent
from messages import CommodityStock, StockFlag, StockRequest, StockResponse

agent = make_agent("ration_seva_stock_validator", "RATION_VALIDATOR_SEED", 8001, "VALIDATOR_MAILBOX")


def lookup(fps_id, commodity=None):
    shop = rd.find_shop(fps_id)
    if shop is None:
        return StockResponse(
            found=False,
            fps_id=fps_id,
            commodity_requested=commodity,
            data_time=rd.data_time(),
            message=(f"FPS {fps_id} is not in the dataset ({rd.shop_count()} shops, "
                     f"AP AePDS report of {rd.data_time()})."),
        )

    key = rd.commodity_key(commodity) if commodity else None
    items, flags = [], []
    for c in rd.ration_items(shop, key):
        values = (c["closing"], c["received"], c["issued"])
        if any(v < 0 for v in values):
            flags.append(StockFlag(commodity=c["commodity"], flag="NEGATIVE_VALUE",
                                   severity="error", message="Negative quantity in report"))
        status = rd.classify(c["closing"], c["issued"])
        if status != c["status"]:
            flags.append(StockFlag(commodity=c["commodity"], flag="STATUS_MISMATCH", severity="warning",
                                   message=f"Report status {c['status']}, recomputed {status}"))
        items.append(CommodityStock(
            commodity=c["commodity"], unit=c["unit"], closing=c["closing"],
            received=c["received"], issued=c["issued"],
            available=round(c["closing"] + c["issued"], 3), status=status,
        ))

    names = {i.commodity for i in items}
    flags += [StockFlag(commodity=f["commodity"], flag=f["flag"], severity=f["severity"], message=f["message"])
              for f in shop.get("flags", []) if f["commodity"] in names]

    if key and not items:
        message = f"FPS {fps_id} has no {commodity} in this report (not allotted)."
    else:
        message = f"{len(items)} ration item(s) reported for FPS {fps_id}."

    return StockResponse(
        found=True, fps_id=shop["fps_id"], commodity_requested=key,
        district=shop["district"], afso=shop["afso"],
        data_time=shop["data_time"], report_date=shop["report_date"],
        source=shop["source"], is_live=shop.get("is_live", False),
        commodities=items, flags=flags, message=message,
    )


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Loaded {rd.shop_count()} shops from {rd.DATA_PATH} (data_time {rd.data_time()})")


@agent.on_message(model=StockRequest, replies={StockResponse})
async def handle_stock_request(ctx: Context, sender: str, msg: StockRequest):
    ctx.logger.info(f"Stock request fps_id={msg.fps_id} commodity={msg.commodity}")
    response = lookup(msg.fps_id.strip(), msg.commodity)
    ctx.logger.info(f"-> found={response.found} items={len(response.commodities)}")
    await ctx.send(sender, response)


if __name__ == "__main__":
    agent.run()
