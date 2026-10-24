
import os
from datetime import datetime, timezone

from dotenv import load_dotenv
from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    TextContent,
    chat_protocol_spec,
)

from messages import StockRequest, StockResponse, ValidatedStock

load_dotenv()

# --------------------------------------------------
# RATION SEVA — SAMPLE DATA
# Demonstration data only, NOT live government data.
# --------------------------------------------------

SAMPLE_STOCK = {
    "rice": {
        "opening": 300,
        "received": 100,
        "issued": 150,
        "closing": 250,
        "report_date": "2026-10-20",
    },
    "wheat": {
        "opening": 100,
        "received": 20,
        "issued": 40,
        "closing": 80,
        "report_date": "2026-10-20",
    },
}


def validate_stock_values(opening, received, issued, closing):
    """Check stock quantities and the stock-balance equation."""

    values = [opening, received, issued, closing]

    if any(
        not isinstance(value, (int, float)) or isinstance(value, bool)
        for value in values
    ):
        return False, "Invalid: stock quantities must be numbers."

    if any(value < 0 for value in values):
        return False, "Invalid: stock quantities cannot be negative."

    expected_closing = opening + received - issued

    if expected_closing != closing:
        return (
            False,
            f"FAIL: expected closing stock {expected_closing}, "
            f"but the reported closing stock is {closing}.",
        )

    return (
        True,
        f"PASS: {opening} + {received} - {issued} = {closing}.",
    )


def get_stock_report(commodity):
    """Return the sample stock and its validation result."""

    commodity = commodity.lower().strip()

    if commodity not in SAMPLE_STOCK:
        raise ValueError("Only sample rice and wheat reports are available.")

    report = SAMPLE_STOCK[commodity]

    passed, result = validate_stock_values(
        report["opening"],
        report["received"],
        report["issued"],
        report["closing"],
    )

    stock = ValidatedStock(
        commodity=commodity,
        opening=report["opening"],
        received=report["received"],
        issued=report["issued"],
        closing=report["closing"],
        report_date=report["report_date"],
        validation_passed=passed,
    )

    report_text = (
        f"Ration Seva — {commodity.title()} stock report\n"
        f"Report date: {report['report_date']}\n"
        f"Opening stock: {report['opening']} kg\n"
        f"Received: {report['received']} kg\n"
        f"Issued: {report['issued']} kg\n"
        f"Reported closing stock: {report['closing']} kg\n\n"
        f"Validation: {result}\n\n"
        "Important: These are sample demonstration figures, not live "
        "government data or confirmation of physical shop stock."
    )

    return stock, report_text


def get_response(user_text):
    """Respond to chat messages about sample rice or wheat stock."""

    text = user_text.lower()

    if "rice" in text:
        commodity = "rice"
    elif "wheat" in text:
        commodity = "wheat"
    else:
        return "Welcome to Ration Seva! Ask me to check rice or wheat stock."

    try:
        _, report_text = get_stock_report(commodity)
        return report_text
    except ValueError as exc:
        return str(exc)


# --------------------------------------------------
# STOCK VALIDATOR AGENT — PORT 8001
# --------------------------------------------------

agent = Agent(
    name="ration_seva_agent",
    seed=os.environ["RATION_VALIDATOR_SEED"],
    port=8001,
    mailbox=True,
)

chat_protocol = Protocol(spec=chat_protocol_spec)


# Structured request from the Coordinator.
@agent.on_message(model=StockRequest, replies={StockResponse})
async def handle_stock_request(
    ctx: Context,
    sender: str,
    msg: StockRequest,
):
    ctx.logger.info(f"Received stock request for {msg.commodity}")

    try:
        stock, report_text = get_stock_report(msg.commodity)

        response = StockResponse(
            report=report_text,
            stock=stock,
        )

        await ctx.send(sender, response)
        ctx.logger.info(
            f"Sent stock validation for {msg.commodity}: "
            f"{stock.validation_passed}"
        )

    except ValueError as exc:
        ctx.logger.warning(str(exc))
        # The current StockResponse schema requires a stock object.
        # Unsupported commodities are logged rather than fabricated.


# Existing Agentverse chat protocol.
@chat_protocol.on_message(ChatMessage)
async def handle_chat_message(
    ctx: Context,
    sender: str,
    msg: ChatMessage,
):
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged_msg_id=msg.msg_id,
        ),
    )

    user_text = " ".join(
        item.text
        for item in msg.content
        if isinstance(item, TextContent)
    ).strip()

    ctx.logger.info(f"Received chat message: {user_text}")

    reply = get_response(user_text)

    await ctx.send(
        sender,
        ChatMessage(
            timestamp=datetime.now(timezone.utc),
            msg_id=ctx.new_uuid(),
            content=[
                TextContent(text=reply),
                EndSessionContent(),
            ],
        ),
    )

    ctx.logger.info("Sent Ration Seva chat response.")


@chat_protocol.on_message(ChatAcknowledgement)
async def handle_chat_acknowledgement(
    ctx: Context,
    sender: str,
    msg: ChatAcknowledgement,
):
    ctx.logger.info(f"Chat acknowledgement received from {sender}")


agent.include(chat_protocol, publish_manifest=True)


if __name__ == "__main__":
    agent.run()
