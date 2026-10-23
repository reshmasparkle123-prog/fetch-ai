from uagents import Agent, Context, Model

class StockRequest(Model):
    shop_id: str
    commodity: str

agent = Agent(
    name="ration_seva_agent",
    seed="fetch-ai-ration-seva-demo-seed-change-this",
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

if __name__ == "__main__":
    agent.run()
