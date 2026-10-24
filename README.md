# 🌾 Ration Seva — Know Before You Go

> **Right Information. Right Ration. Right Time.**

Ration Seva is an AI-powered ration assistance project designed to help beneficiaries check reported Fair Price Shop (FPS) stock information before travelling to collect essential food grains.

Built for **Fetch-A-Thon 3.0 at Presidency University, Bengaluru**, Ration Seva uses AI agents, stock validation, and conversational assistance to help people make better-informed decisions about ration-shop visits.

## 🔗 Project Links

| Resource | Link |
|---|---|
| 💬 ASI:One | [Open ASI:One](https://asi1.ai/) |
| 💬 Working ASI Demo | Pending successful end-to-end conversation |
| 🤖 Agentverse Agent Profile | [Ration Seva Shortage Analyst](https://agentverse.ai/agents/details/agent1qdj3kmjycxdfj6lp23yzmzg567a78ftn2gk9q5eyqqx8nwm8qy8qkfth24c) |
| 🐍 Shortage Analyst Agent Address | `agent1qdj3kmjycxdfj6lp23yzmzg567a78ftn2gk9q5eyqqx8nwm8qy8qkfth24c` |
| 📦 GitHub Repository | [reshmasparkle123-prog/fetch-ai](https://github.com/reshmasparkle123-prog/fetch-ai) |

**Note:** The shortage analyst is registered on Agentverse and has shown Active status with Mailbox enabled. A successful ASI:One conversation and the complete multi-agent workflow must be tested before claiming they are fully verified.

## 🎯 The Problem

Beneficiaries who depend on India's Public Distribution System (PDS) may travel to a Fair Price Shop without knowing the latest reported availability of essential commodities.

This can lead to:

- Unnecessary trips to ration shops.
- Time and potential wages lost while travelling or waiting.
- Uncertainty caused by outdated or incomplete stock information.
- Difficulty understanding stock reports and deciding what to do next.

Access to essential food should not involve avoidable uncertainty.

## 💡 Our Solution

**Ration Seva aims to help people make better-informed decisions before visiting their ration shop.**

Through a conversational AI interface, users can ask about shop and commodity stock. The intended workflow retrieves available stock records, validates the reported quantities, and explains the results in simple language.

### Key capabilities

- 🔎 **Stock lookup:** Retrieve reported commodity quantities for a specified shop when a suitable data source is configured.
- 🧮 **Stock validation:** Check whether reported quantities are arithmetically consistent.
- 🕒 **Freshness awareness:** Display report dates and warn about outdated information when dates are available.
- 🛡️ **Responsible responses:** Handle missing, unknown, or inconsistent records without inventing data.
- 💬 **Conversational assistance:** Support natural-language questions through the intended ASI integration.
- 🤖 **Agent-based execution:** Use specialised agents and coordination where implemented and verified.

## ⚙️ How It Works

The intended workflow is:

```text
              BENEFICIARY
                   |
                   v
             ASI:One Chat
                   |
                   v
          Ration Seva Agent
                   |
                   v
          Stock Lookup Tool
                   |
                   v
          Stock Validation
          - Quantity checks
          - Arithmetic checks
          - Date and completeness
                   |
                   v
          Clear Explanation
          + Source + Warnings
                   |
                   v
        INFORMED USER DECISION
```

The diagram represents the intended architecture. The actual implementation may differ depending on which components and integrations are configured and running.

## 🧠 Agent Architecture

### 1. Stock Validation Agent

Checks stock quantities and identifies arithmetic inconsistencies in the records it receives.

### 2. Shortage Analyst Agent

The registered `ration_seva_shortage_analyst` agent is intended to evaluate validated ration-shop stock records and identify potential low-stock signals.

### 3. Coordinator

The coordinator is intended to route requests between specialised agents and combine their responses. End-to-end coordination should be claimed as operational only after real agent-to-agent communication has been tested.

### 4. Conversational Interface

ASI:One is the intended conversational interface for beneficiaries to interact with the system.

## 🧮 Stock Calculation

When all required values are available:

**Expected closing stock = Opening stock + Received stock − Issued stock**

For example:

- Opening stock: 300 kg
- Received stock: 100 kg
-
