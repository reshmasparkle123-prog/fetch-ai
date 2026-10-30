"""
RationSeva Shortage Analyst (port 8003) - internal agent, called by the Coordinator.

Rules (same as the ingest that produced data/summary.json):
  LOW           closing < 10% of this month's available stock (closing + issued)
  OUT_OF_STOCK  closing ~ 0 (<= 0.01)

"Where else can I go?": for a LOW/OUT (or explicitly asked) commodity, suggests up
to 3 other shops in the same AFSO that have it AVAILABLE in the same snapshot.
"""

from uagents import Context

import ration_data as rd
from common import make_agent
from messages import AlternativeShop, CommodityAssessment, ShortageAnalysis, ShortageRequest

agent = make_agent("ration_seva_shortage_analyst", "SHORTAGE_ANALYST_SEED", 8003, "SHORTAGE_ANALYST_MAILBOX")


def analyse(msg: ShortageRequest) -> ShortageAnalysis:
    assessments = []
    for c in msg.commodities:
        available = c.closing + c.issued
        assessments.append(CommodityAssessment(
            commodity=c.commodity, unit=c.unit, closing=c.closing, available=round(available, 3),
            percent_left=round(100 * c.closing / available, 1) if available > 0 else 0.0,
            status=rd.classify(c.closing, c.issued),
        ))

    # Which commodities need alternatives:
    #  - user asked "where else?"      -> the asked commodity (any status), else every LOW/OUT item
    #  - plain stock check of one item -> only if that item is LOW/OUT
    short = [a for a in assessments if a.status != "AVAILABLE"]
    if msg.want_alternatives:
        targets = assessments if msg.commodity_requested else short
    else:
        targets = short if msg.commodity_requested else []

    alternatives = {}
    for a in targets:
        alternatives[a.commodity] = [
            AlternativeShop(fps_id=s["fps_id"], afso=s["afso"], commodity=c["commodity"],
                            unit=c["unit"], closing=c["closing"], status="AVAILABLE")
            for s, c in rd.alternatives(msg.fps_id, a.commodity)
        ]

    lines = [f"{a.commodity}: {a.status} ({a.closing:g} {a.unit}, {a.percent_left}% of month's stock)"
             for a in assessments]
    for name, shops in alternatives.items():
        lines.append(f"Alternatives for {name} in {msg.afso}: "
                     + (", ".join(s.fps_id for s in shops) or "none with it AVAILABLE"))

    return ShortageAnalysis(fps_id=msg.fps_id, afso=msg.afso, assessments=assessments,
                            alternatives=alternatives, data_time=rd.data_time(),
                            analysis="\n".join(lines))


@agent.on_message(model=ShortageRequest, replies={ShortageAnalysis})
async def handle_shortage_request(ctx: Context, sender: str, msg: ShortageRequest):
    ctx.logger.info(f"Shortage request fps_id={msg.fps_id} commodity={msg.commodity_requested} "
                    f"alternatives={msg.want_alternatives}")
    result = analyse(msg)
    ctx.logger.info(result.analysis.replace("\n", " | "))
    await ctx.send(sender, result)


if __name__ == "__main__":
    agent.run()
