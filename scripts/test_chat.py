"""
Local chat test: talks to the Coordinator over the same chat protocol ASI:One uses.

    python scripts/run_local.py --no-mailbox        # in one terminal
    python scripts/test_chat.py                     # all scenarios
    python scripts/test_chat.py stock notice_te     # just some
    python scripts/test_chat.py weighing --photo path/to/scale.png

Photos are served from a throw-away local HTTP server and sent as ResourceContent,
exactly like an ASI:One attachment with a URL. `weighing_bytes` sends the same photo
as a data: URI, which exercises the path where the Coordinator forwards the bytes
itself (what happens with Agentverse-storage attachments).
Results are printed and written to logs/test_chat_results.md.
"""

import argparse
import asyncio
import base64
import functools
import http.server
import os
import sys
import threading
import time
from datetime import datetime, timezone
from uuid import uuid4

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from dotenv import load_dotenv  # noqa: E402
from uagents import Agent, Context, Protocol  # noqa: E402
from uagents.crypto import Identity  # noqa: E402
from uagents_core.contrib.protocols.chat import (  # noqa: E402
    ChatAcknowledgement, ChatMessage, Resource, ResourceContent, TextContent, chat_protocol_spec,
)

load_dotenv(os.path.join(ROOT, ".env"))
COORDINATOR = Identity.from_seed(os.environ["RATION_COORDINATOR_SEED"], 0).address

SCENARIOS = {
    "stock": [("Is rice available at shop 0306122?", None)],
    "alternatives": [("Rice is low at my shop, where else can I go?", None), ("0306122", None)],
    "notice_te": [("Make a Telugu stock notice for 0306122", None)],
    "weighing": [("Check my ration weight", "photo"), ("shop 0306122, entitled 70 kg rice", None), ("confirm", None)],
    "weighing_bytes": [("Check my ration weight at shop 0306122, entitled 65 kg rice", "photo_bytes")],
    "weighing_no_photo": [("Check my ration weight", None),
                          ("I got 18 kg instead of 20 kg rice at shop 0306122", None), ("cancel", None)],
    "unknown_fps": [("Is rice available at shop 9999999?", None)],
    "telugu_stock": [("0306122 షాప్‌లో బియ్యం ఉందా?", None)],
    "hindi_alternatives": [("मेरी दुकान 0306122 में चावल कम है, और कहाँ मिलेगा?", None)],
    "agent_down": [("Is rice available at shop 0306122?", None)],   # run with the Stock Validator stopped
}
DEFAULT = ["stock", "alternatives", "notice_te", "weighing", "weighing_bytes", "weighing_no_photo",
           "unknown_fps", "telugu_stock", "hindi_alternatives"]


def serve(directory, port=8099):
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=directory)
    handler.log_message = lambda *a: None
    server = http.server.ThreadingHTTPServer(("127.0.0.1", port), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return f"http://127.0.0.1:{port}"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("scenarios", nargs="*", default=DEFAULT)
    ap.add_argument("--photo", help="scale photo (default: ../ration-seva-/scripts/scale.png)")
    ap.add_argument("--timeout", type=int, default=150)
    args = ap.parse_args()

    photo = os.path.abspath(args.photo or os.path.join(ROOT, "..", "ration-seva-", "scripts", "scale.png"))
    photo_url = f"{serve(os.path.dirname(photo))}/{os.path.basename(photo)}" if os.path.exists(photo) else None
    photo_mime = "image/png" if photo.lower().endswith(".png") else "image/jpeg"

    client = Agent(name="ration_seva_test_client", seed=f"ration-seva-test-client-{uuid4()}", port=8010,
                   endpoint=["http://127.0.0.1:8010/submit"])
    chat = Protocol(spec=chat_protocol_spec)
    inbox: asyncio.Queue = asyncio.Queue()
    out_lines = []

    def log(line=""):
        print(line, flush=True)
        out_lines.append(line)

    def message(text, kind):
        content = [TextContent(type="text", text=text)] if text else []
        if kind:
            if not photo_url:
                raise SystemExit(f"photo not found: {photo}")
            uri = photo_url
            if kind == "photo_bytes":
                with open(photo, "rb") as f:
                    uri = f"data:{photo_mime};base64,{base64.b64encode(f.read()).decode()}"
            content.append(ResourceContent(type="resource", resource_id=uuid4(),
                                           resource=Resource(uri=uri, metadata={"mime_type": photo_mime})))
        return ChatMessage(timestamp=datetime.now(timezone.utc), msg_id=uuid4(), content=content)

    @chat.on_message(ChatMessage)
    async def on_reply(ctx: Context, sender: str, msg: ChatMessage):
        await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.now(timezone.utc),
                                                   acknowledged_msg_id=msg.msg_id))
        await inbox.put(msg)

    @chat.on_message(ChatAcknowledgement)
    async def on_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
        pass

    client.include(chat)

    async def run(ctx: Context):
        await asyncio.sleep(3)
        log(f"# RationSeva local chat test — {datetime.now():%Y-%m-%d %H:%M}\n\nCoordinator: `{COORDINATOR}`")
        for name in args.scenarios:
            log(f"\n## {name}")
            for text, kind in SCENARIOS[name]:
                log(f"\n**USER:** {text}" + (f"  _[attached {os.path.basename(photo)} as "
                                             f"{'data: URI' if kind == 'photo_bytes' else 'URL'}]_" if kind else ""))
                started = time.time()
                await ctx.send(COORDINATOR, message(text, kind))
                try:
                    reply = await asyncio.wait_for(inbox.get(), timeout=args.timeout)
                except asyncio.TimeoutError:
                    log(f"\n**COORDINATOR:** _(no reply within {args.timeout}s)_")
                    continue
                body = "\n".join(c.text for c in reply.content if isinstance(c, TextContent))
                ended = any(getattr(c, "type", "") == "end-session" for c in reply.content)
                log(f"\n**COORDINATOR** ({time.time() - started:.1f}s, end_session={ended}):\n\n{body}")
        with open(os.path.join(ROOT, "logs", "test_chat_results.md"), "w", encoding="utf-8") as f:
            f.write("\n".join(out_lines) + "\n")
        os._exit(0)

    @client.on_event("startup")
    async def startup(ctx: Context):
        asyncio.create_task(run(ctx))

    os.makedirs(os.path.join(ROOT, "logs"), exist_ok=True)
    client.run()


if __name__ == "__main__":
    main()
