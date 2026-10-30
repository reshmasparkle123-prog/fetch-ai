# RationSeva × Fetch.ai — build notes

_Branch `asad/real-data-agents` · 30 Oct 2026_

## What we built

A five-agent uAgents system that a beneficiary uses entirely inside one ASI:One chat, in English, Telugu or Hindi. It covers stock checks, "where else can I go?", Cloudinary stock posters and Cloudinary-OCR weighing checks. It runs on real data: the AP AePDS report for 480 shops (snapshot 2026-10-20 22:00) and our live Cloudinary backend (ration-seva.onrender.com).

## Key decisions

### Why multi-agent
- **One job per agent, one message type per agent.** Stock lookup, shortage analysis, poster rendering and weighing checks have different dependencies (local data vs. the Cloudinary backend) and different failure modes. Separate agents let each one fail, restart and be tested on its own.
- **Graceful degradation is possible because of the split.** If the Notice Agent is down, the Coordinator still returns the real stock as text. If the Shortage Analyst is down, the user still gets the report status. One monolith would fail all at once.
- **Typed contracts** (`messages.py`) make each hop testable and stop any agent from "talking its way" into made-up data. An unknown shop comes back as `found=False`, not a guess.

### Why the Coordinator is the only chat-protocol agent
- ASI:One should see **one** RationSeva agent with one manifest and one conversation. Before, `main.py` (the validator) also exposed the chat protocol, so two agents could answer the same user with different logic.
- The chat protocol is free text. Internal agents should take structured input only. Language detection, entity extraction, follow-up questions and conversation state (pending question, complaint awaiting confirmation) all live in one place.
- Only the Coordinator needs an Agentverse mailbox. The internal agents use local endpoints, so there is one login, one Inspector connection, and fewer moving parts.

### How the agents reuse our Cloudinary features
- **Notice Agent → `POST /notice`**: Cloudinary renders the poster with text overlays, using uploaded Noto Sans Telugu / Devanagari fonts, `g_auto` cropping, `f_auto,q_auto` and a signed URL. The Coordinator puts the image inline in chat, so the beneficiary gets something to forward on WhatsApp, not a paragraph.
- **Weighing Agent → `POST /scale-check`**: Cloudinary uploads the photo, `adv_ocr` reads the scale display, and the image is stamped with FPS id + "WEIGHING PROOF" + IST time. The stamped proof URL goes straight into the complaint draft as evidence.
- We **reused the backend instead of calling Cloudinary from the agents**. Credentials stay in one place (Render env), all the OCR heuristics (ignore bag labels, model numbers, `NEEDS_REVIEW` upper bound) are shared with the web app, and the agents need no secrets.

### Other decisions
- **Rule-based language understanding, not an LLM.** Keyword/regex parsing in en/te/hi is predictable and testable, and it can't invent a shop number. Missing information becomes a follow-up question.
- **Never auto-file complaints.** `SHORT_WEIGHT` produces a draft. The user must reply "confirm", and even then we only hand back the final text to send.
- **Status rule matches the ingest pipeline** (LOW < 10% of closing + issued, OUT ≤ 0.01). We checked it against all 2,232 commodity rows: it agrees with every reported status.
- **Alternatives by AFSO.** The data has no mandal or GPS, so "nearby" means same AFSO, sorted by stock.

## Challenges hit and fixes

| Challenge | Fix |
|---|---|
| Old `ChatAcknowledgement(acknowledged=True)` doesn't match the protocol model | `ChatAcknowledgement(timestamp=…, acknowledged_msg_id=msg.msg_id)`; final replies add `EndSessionContent`; follow-up questions don't end the session. |
| **`ctx.send_and_receive` returns a tuple `(msg, status)`**, but the old code treated it as the message, so the workflow could never have worked | Unpack the tuple, check `status`, retry once, then fall back. |
| Old stock answers came from a hardcoded rice/wheat sample | Stock Validator now reads `data/summary.json`. We checked it has 480 records / 480 unique shops before using it, because an older root copy once had only 1 record. |
| `test_sender.py` used a different `StockRequest` schema and the validator's port (8001) | Removed; replaced by `scripts/test_chat.py`, which speaks the real chat protocol. |
| Render free tier sleeps (~33–50 s cold start) but agent calls time out at 30 s | Backend agents ping `/health` at startup. Each backend call times out at 25 s with `retryable=True`, and the Coordinator retries once, by which time the backend is warm. |
| ASI:One attachments live in Agentverse storage, and only the **receiving** agent (Coordinator) is granted read access | The Coordinator downloads the asset with its own identity and forwards the bytes; public URLs are passed through. Also: `ExternalStorage` without `storage_url` hits a missing config attribute (`storage_endpoint`), so we pass `AgentverseConfig().storage_api` explicitly. |
| `summary.json` lists "10KG BAG" / "15KG BAG" (empty sacks returned by the shop) as AVAILABLE | Filtered with the same packaging regex the ingest uses, so they never appear as ration. |
| Python 3.14 is too new for uagents | Project venv on Python 3.12; documented in the README. |
| The local launcher shut every agent down when one died, so the agent-down case couldn't be tested | The launcher now reports the dead agent and keeps the rest running. |
| The notice fallback showed "analysis unavailable" even though the analyst was up | The fallback now calls the analyst too, so that note appears only when it's really down. |

## Test results (local, real backend)

All scenarios passed, 14/14 replies: stock check 0306122, alternatives with a follow-up for the missing shop number, Telugu notice (Cloudinary poster), weighing by photo URL (OCR 68.5 kg vs 70 → SHORT_WEIGHT → draft → confirm), weighing by forwarded bytes (OK), typed-weight check → cancel, unknown FPS 9999999, Telugu stock question, Hindi alternatives. Agent-down: validator stopped → clear "stock service not responding"; notice agent stopped → text fallback with real stock. Typical latency is 2–3 s for data answers and 6–9 s for Cloudinary calls. Full transcript: `docs/TEST_RESULTS.md`.

## Learnings

- **Read the SDK signatures, not old examples.** Both chat-protocol bugs (ack fields, `send_and_receive` tuple) came from code written against assumptions.
- **Verify data before trusting it.** Counting records and comparing our status rule with the reported status took a minute and caught both a past truncated file and the packaging-as-stock issue.
- **Design the failure path first** on free-tier infrastructure: timeouts, one retry, and a useful fallback answer matter more than speed.
- **One public agent and many private ones** keeps the ASI:One experience simple while the internals stay modular.
- **Show, don't tell:** a poster image and a stamped proof photo are what make the Cloudinary features useful to a beneficiary. Text alone would not.

## Next steps
- Wire `POST /proof` (privacy-blurred doorstep-delivery / complaint photos) into a Proof Agent.
- Refresh `summary.json` from newer AePDS reports on a schedule, and warn when the snapshot is old.
- Test ASI:One photo attachments end-to-end after connecting the mailbox.
