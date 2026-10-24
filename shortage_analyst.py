from dotenv import load_dotenv
load_dotenv()


import os

from uagents import Agent, Context
from messages import ValidatedStock, ShortageAnalysis

SEED = os.environ.get("SHORTAGE_ANALYST_SEED")

if not SEED:
    raise RuntimeError("Set SHORTAGE_ANALYST_SEED before starting.")

agent = Agent(
    name="ration_seva_shortage_analyst",
    seed=SEED,
    port=8003,
    mailbox=True,
)


@agent.on_message(model=ValidatedStock, replies={ShortageAnalysis})
async def analyse_stock(ctx: Context, sender: str, msg: ValidatedStock):
    if not msg.validation_passed:
        result = "Stock validation failed. No analysis performed."
    elif msg.closing <= 0:
        result = f"{msg.commodity}: zero closing stock in the sample data."
    elif msg.closing < 50:
        result = f"{msg.commodity}: low-stock signal in the sample data."
    else:
        result = f"{msg.commodity}: no low-stock signal under the sample threshold."

    result += (
        "\nIllustrative only. This does not confirm a real-world "
        "shortage or current physical shop stock."
    )

    await ctx.send(
        sender,
        ShortageAnalysis(analysis=result, illustrative_only=True),
    )


if __name__ == "__main__":
    agent.run()

