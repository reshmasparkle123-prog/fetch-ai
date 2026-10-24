
import os
import uuid
import logging
from datetime import datetime, timezone

from dotenv import load_dotenv
from uagents import Agent, Context, Protocol

from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    TextContent,
    chat_protocol_spec,
)

from messages import StockRequest, StockResponse, ShortageAnalysis


load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ration_seva_coordinator")


# --------------------------------------------------
# Environment configuration
# --------------------------------------------------

SEED = os.getenv("RATION_COORDINATOR_SEED")
STOCK_VALIDATOR_ADDRESS = os.getenv("STOCK_VALIDATOR_ADDRESS")
SHORTAGE_ANALYST_ADDRESS = os.getenv("SHORTAGE_ANALYST_ADDRESS")

if not SEED:
    raise ValueError("RATION_COORDINATOR_SEED is missing from .env")

if not STOCK_VALIDATOR_ADDRESS:
    raise ValueError("STOCK_VALIDATOR_ADDRESS is missing from .env")

if not SHORTAGE_ANALYST_ADDRESS:
    raise ValueError("SHORTAGE_ANALYST_ADDRESS is missing from .env")


# --------------------------------------------------
# Coordinator agent
# --------------------------------------------------

agent = Agent(
    name="ration_seva_coordinator",
    seed=SEED,
    port=8002,
    mailbox=True,
)

chat_protocol = Protocol(spec=chat_protocol_spec)


# --------------------------------------------------
# Helper functions
# --------------------------------------------------

def extract_text(message: ChatMessage) -> str:
    """Extract text content from an incoming chat message."""
    return " ".join(
        item.text
        for item in message.content
        if isinstance(item, TextContent)
    ).strip()


def choose_commodity(question: str) -> str:
    """Choose a commodity based on the user's question."""
    question = question.lower()

    if "wheat" in question:
        return "Wheat"

    if "rice" in question:
        return "Rice"

    return "Rice"


def make_chat_message(text: str) -> ChatMessage:
    return ChatMessage(
        timestamp=datetime.now(timezone.utc),
        msg_id=str(uuid.uuid4()),
        content=[TextContent(text=text)],
    )


# --------------------------------------------------
# Incoming chat messages
# --------------------------------------------------

@chat_protocol.on_message(ChatMessage)
async def handle_chat_message(
    ctx: Context,
    sender: str,
    msg: ChatMessage,
):
    question = extract_text(msg)

    logger.info(
        "Received question from %s: %s",
        sender,
        question,
    )

    # Acknowledge the incoming chat message.
    await ctx.send(
        sender,
        ChatAcknowledgement(
            timestamp=datetime.now(timezone.utc),
            acknowledged=True,
        ),
    )

    if not question:
        await ctx.send(
            sender,
            make_chat_message(
                "Please ask a question about reported ration-shop stock."
            ),
        )
        return

    commodity = choose_commodity(question)

    try:
        # Step 1: Request stock validation.
        logger.info(
            "Requesting stock validation for %s",
            commodity,
        )

        stock_response = await ctx.send_and_receive(
            STOCK_VALIDATOR_ADDRESS,
            StockRequest(commodity=commodity),
            response_type=StockResponse,
            timeout=30,
        )

        if stock_response is None:
            raise TimeoutError(
                "Stock validator did not respond."
            )

        logger.info("Stock validator responded.")

        # Step 2: Request shortage analysis.
        logger.info("Requesting shortage analysis.")

        analysis_response = await ctx.send_and_receive(
            SHORTAGE_ANALYST_ADDRESS,
            stock_response.stock,
            response_type=ShortageAnalysis,
            timeout=30,
        )

        if analysis_response is None:
            raise TimeoutError(
                "Shortage analyst did not respond."
            )

        logger.info("Shortage analyst responded.")

        stock = stock_response.stock

        validation_status = (
            "Passed"
            if stock.validation_passed
            else "Failed"
        )

        reply = (
            f"Ration Seva — {stock.commodity} stock report\n\n"
            f"Opening stock: {stock.opening}\n"
            f"Received: {stock.received}\n"
            f"Issued: {stock.issued}\n"
            f"Reported closing stock: {stock.closing}\n"
            f"Report date: {stock.report_date}\n"
            f"Validation: {validation_status}\n\n"
            f"Shortage analysis:\n{analysis_response.analysis}\n\n"
            "Important: This report reflects sample or reported data. "
            "It does not confirm current physical stock at the shop."
        )

    except Exception as exc:
        logger.exception("Ration Seva workflow failed")

        reply = (
            "Ration Seva could not complete the stock-check workflow.\n"
            f"Error: {type(exc).__name__}: {exc}\n\n"
            "Please check that both downstream agents are running, "
            "their addresses are correct, and messages can be exchanged."
        )

    await ctx.send(sender, make_chat_message(reply))

    logger.info(
        "Sent workflow result to %s",
        sender,
    )


# --------------------------------------------------
# Incoming chat acknowledgements
# --------------------------------------------------

@chat_protocol.on_message(ChatAcknowledgement)
async def handle_chat_acknowledgement(
    ctx: Context,
    sender: str,
    msg: ChatAcknowledgement,
):
    logger.info(
        "Received acknowledgement from %s: acknowledged=%s",
        sender,
        msg.acknowledged,
    )


# --------------------------------------------------
# Register protocol
# --------------------------------------------------

agent.include(
    chat_protocol,
    publish_manifest=True,
)


if __name__ == "__main__":
    agent.run()
