import asyncio
asyncio.set_event_loop(asyncio.new_event_loop())

from uagents import Agent, Context, Model
from stock_tools import validate_stock

class StockRequest(Model):
    shop_id: str
    commodity: str

agent = Agent(
    name="ration_seva_agent",
    seed="fetch-ai-ration-seva-demo-seed-change-this",
    port=8000,
    endpoint=["http://127.0.0.1:8000/submit"],
)

@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Ration Seva AI agent is online!")

@agent.on_message(model=StockRequest)
async def handle_stock_request(ctx: Context, sender: str, msg: StockRequest):
    ctx.logger.info(
        f"Stock request received: shop={msg.shop_id}, "
        f"commodity={msg.commodity}"
    )
    result = validate_stock(
        opening=100,
        received=50,
        issued=30,
        closing=120
    )

    ctx.logger.info(f"Stock validation result: {result}")

if __name__ == "__main__":
    agent.run()
