"""
RationSeva Notice Agent (port 8004) - internal agent, called by the Coordinator.

Calls the RationSeva backend POST /notice, which renders a shareable stock-notice
poster for one shop with Cloudinary (text overlays in Telugu / Hindi / English
fonts, auto format + quality). Returns the Cloudinary image URL.
"""

from uagents import Context

from common import BackendError, backend_post, make_agent, warm_backend
from messages import NoticeRequest, NoticeResponse

LANGUAGES = {"te", "hi", "en"}

agent = make_agent("ration_seva_notice_agent", "NOTICE_AGENT_SEED", 8004, "NOTICE_AGENT_MAILBOX")


@agent.on_event("startup")
async def startup(ctx: Context):
    await warm_backend(ctx.logger)


@agent.on_message(model=NoticeRequest, replies={NoticeResponse})
async def handle_notice_request(ctx: Context, sender: str, msg: NoticeRequest):
    language = msg.language if msg.language in LANGUAGES else "te"
    ctx.logger.info(f"Notice request fps_id={msg.fps_id} language={language}")
    base = dict(fps_id=msg.fps_id, language=language)
    try:
        result = await backend_post("/notice", {"fps_id": msg.fps_id, "language": language})
        response = NoticeResponse(ok=True, url=result["url"], items=result.get("items", []),
                                  data_time=result.get("data_time"), **base)
    except BackendError as e:
        ctx.logger.warning(f"/notice failed: {e} (status={e.status}, retryable={e.retryable})")
        response = NoticeResponse(ok=False, error=str(e), not_found=e.status == 404,
                                  retryable=e.retryable, **base)
    ctx.logger.info(f"-> ok={response.ok} url={'yes' if response.url else 'no'}")
    await ctx.send(sender, response)


if __name__ == "__main__":
    agent.run()
