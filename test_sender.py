
import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())
from uagents import Agent, Context, Model

class StockRequest(Model):
    shop_id: str
    commodity: str

sender_agent = Agent(
    name="stock_test_sender",
    seed="ration-seva-test-sender-seed-change-this",
    port=8001,
    endpoint=["http://127.0.0.1:8001/submit"],
)

@sender_agent.on_event("startup")
async def startup(ctx: Context):
    await ctx.send(
        "agent1qvn502s0j4vxgajjm962vng46vr4ryk2f6emsnsafxt8dku95cn9gnfd42t",
        StockRequest(shop_id="SHOP001", commodity="rice"),
    )
    ctx.logger.info("Test stock request sent!")

if __name__ == "__main__":
    sender_agent.run()
