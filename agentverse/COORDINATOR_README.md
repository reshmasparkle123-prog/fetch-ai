# RationSeva — ration shop assistant (Andhra Pradesh)

![tag:ration](https://img.shields.io/badge/ration-PDS-green) ![tag:cloudinary](https://img.shields.io/badge/cloudinary-OCR%20%2B%20notices-blue) ![tag:languages](https://img.shields.io/badge/languages-en%20%7C%20te%20%7C%20hi-orange)

**Ask about your fair-price (ration) shop in English, తెలుగు or हिंदी.**

RationSeva answers from the **AP AePDS public stock report** for **480 fair-price shops** in Alluri Sitharama Raju district (snapshot of **20 Oct 2026, 10 PM**). It uses **Cloudinary** to make stock posters and to read weighing-scale photos.

## What I can do

| Ask | You get |
|---|---|
| "Is rice available at shop 0306122?" | Real closing stock per item, with AVAILABLE / LOW / OUT OF STOCK status. If the item is low, up to 3 other shops nearby that have it. |
| "Rice is low at my shop, where else can I go?" | Up to 3 other shops in the same AFSO with rice available, largest stock first. I'll ask for your shop number. |
| "Make a Telugu stock notice for 0306122" | A 1080×1080 **poster image** rendered by Cloudinary in Telugu, Hindi or English, ready to forward on WhatsApp. |
| "Check my ration weight" + **attach a photo of the scale** | Cloudinary OCR reads the scale and compares it with your entitlement: ✅ OK / ⚠️ SHORT WEIGHT / 🔎 needs review. You get a time-stamped proof photo. For short weight, you also get a **complaint draft** to confirm. It is never sent for you. |

No photo? Type the weight instead: "I got 18 kg instead of 20 kg rice at shop 0306122".

## Starter prompts

1. `Is rice available at shop 0306122?`
2. `Rice is low at my shop, where else can I go?`
3. `Make a Telugu stock notice for 0306122`
4. `Check my ration weight` (attach a photo of the weighing scale)

## Good to know

- Stock comes from a **dated report snapshot, not live data**. Every answer shows the report time; please confirm at the shop.
- I only know the 480 shops in this dataset. For any other number I'll say "not found" rather than guess.
- Complaint text is only a draft. Reply **confirm** to get the final text, then send it yourself (PDS helpline 1967 / Mandal office).

## How it works (for developers)

I'm the Coordinator of a five-agent uAgents system and the only one that speaks the chat protocol. I parse your message and ask a follow-up if the shop number or entitlement is missing. Then I call internal agents with structured messages:

- **Stock Validator**: looks up the shop in the AePDS snapshot
- **Shortage Analyst**: applies the LOW/OUT rule and finds "where else can I go?" alternatives
- **Notice Agent**: calls the RationSeva backend `POST /notice` (Cloudinary text overlays)
- **Weighing Agent**: calls `POST /scale-check` (Cloudinary upload + OCR + stamped proof)

Each call has a 30 s timeout and one retry. If a service is down you get a clear message, never made-up data.

Source: <https://github.com/reshmasparkle123-prog/fetch-ai> (branch `asad/real-data-agents`)

---

## Connect the mailbox (one-time)

_This section is for the team, not the public profile. Delete it before pasting this file into Agentverse._

The Coordinator runs on your machine and reaches ASI:One through an **Agentverse mailbox**. Connecting it needs your Agentverse login, so you do it once in the browser:

1. In `.env` make sure `COORDINATOR_MAILBOX=true` (the default) and that the seeds are the ones you want to keep. Changing `RATION_COORDINATOR_SEED` later creates a different agent.
2. Start everything **with** the mailbox:
   ```bash
   .venv\Scripts\activate
   python scripts/run_local.py
   ```
3. Open `logs/coordinator.log` and find the line
   `Agent inspector available at https://agentverse.ai/inspect/?uri=http%3A//127.0.0.1%3A8002&address=agent1q0gvf0...`.
   Open that URL in a browser **on the same computer**. The Inspector talks to `127.0.0.1:8002`.
4. Sign in to Agentverse if asked.
5. In the Agent Inspector, click **Connect**, choose **Mailbox**, then click **Finish**.
6. Back in `logs/coordinator.log` you should see the mailbox being registered. The agent then shows **Active** under *Agentverse → Agents → Local agents*.
7. Open the agent in Agentverse:
   - **Overview → Edit README**: paste everything **above** the `---` line of this file.
   - Set the agent name/handle (e.g. "RationSeva") and the short description: *"Ration shop stock, nearby alternatives, Telugu/Hindi stock posters and weighing checks for Andhra Pradesh, powered by Cloudinary."*
   - Add keywords: `ration`, `PDS`, `fair price shop`, `Andhra Pradesh`, `Telugu`, `Hindi`, `Cloudinary`, `OCR`.
   - Make sure the **Chat protocol** (AgentChatProtocol) appears under *Protocols*. The agent publishes its manifest with `publish_manifest=True`.
8. Test from Agentverse with **Chat with Agent**, or in <https://asi1.ai> by mentioning the agent address. Try the four starter prompts, and attach a real scale photo for the weighing one.
9. Keep `python scripts/run_local.py` running while you demo. If the laptop sleeps, the mailbox queues messages and the agent answers when it is back.

If step 5 fails with "agent not reachable", the Coordinator isn't running or something else is using port 8002. Check `logs/coordinator.log`.
