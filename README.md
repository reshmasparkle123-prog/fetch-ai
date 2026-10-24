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
- Issued stock: 150 kg
- Reported closing stock: 250 kg

Calculation:

`300 + 100 − 150 = 250 kg`

The report is arithmetically consistent because the calculated closing stock matches the reported closing stock.

**Important:** Arithmetic consistency does not prove that the physical stock is available at the shop.

## 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| Python | Agent implementation and stock validation |
| Fetch.ai uAgents framework | Building and running agents |
| Agent Chat Protocol (ACP) | Agent communication, where configured |
| Agentverse | Agent registration and discovery |
| ASI:One | Intended conversational interface |
| Database or stock data source | Stock retrieval, depending on the actual implementation |
| React + Vite | Optional supporting frontend, only if present in the repository |
| Supabase | Optional storage integration, only if configured in the implementation |

The final technology list should match the code and services actually used in the submitted version.

## 🛡️ Data Integrity and Error Handling

Trust and transparency are central to Ration Seva.

| Scenario | Expected behaviour |
|---|---|
| Valid stock record | Return the available quantities and report date |
| Inconsistent quantities | Flag the arithmetic mismatch |
| Negative quantities | Reject or flag invalid data |
| Missing fields | Explain that the record is incomplete |
| Outdated report | Warn that the information may not reflect current conditions |
| Unknown shop ID | Ask the user to verify the identifier |
| Database failure | Return a clear error rather than fabricate results |
| Unverified source | Disclose the source and its verification status |

These are expected behaviours; each should be tested before being marked as implemented.

## 🧪 Testing Checklist

Record the actual outcome of each test before marking it as passed.

- [ ] Valid stock record produces the expected arithmetic result.
- [ ] Inconsistent quantities are flagged.
- [ ] Negative quantities are rejected or flagged.
- [ ] Missing fields are handled safely.
- [ ] An outdated report produces a warning.
- [ ] An unknown shop ID does not produce fabricated information.
- [ ] A data-source failure produces a clear error.
- [ ] The shortage analyst returns an actual response.
- [ ] Agent-to-agent communication is verified, if applicable.
- [ ] An ASI:One conversation completes successfully.
- [ ] The working conversation URL and evidence are saved for submission.

## 🚀 Getting Started

### Prerequisites

- Python version supported by the project's dependencies.
- Git.
- Access to the repository.
- Agentverse account and agent configuration.
- Any database credentials required by the actual implementation.

### 1. Clone the repository

```bash
git clone https://github.com/reshmasparkle123-prog/fetch-ai.git
cd fetch-ai
```

### 2. Create a virtual environment

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

If the repository includes `requirements.txt`:

```bash
pip install -r requirements.txt
```

Use the dependency manager and installation instructions provided by the actual project if they differ.

### 4. Configure environment variables

Create a local `.env` file containing the variables required by the code. For example:

```env
SUPABASE_URL=your_project_url
SUPABASE_KEY=your_appropriate_access_key
```

Only add variables that the implementation actually uses. Agent seeds and credentials must be kept private.

### 5. Run the agents

Use the entry-point filenames and commands defined in the repository. For example, if these files exist and are configured to run independently:

```bash
python main.py
```

```bash
python shortage_analyst.py
```

```bash
python coordinator.py
```

Run each process only as required by the project architecture. Check the actual configuration for ports, addresses, and environment variables before starting multiple agents.

### 6. Run tests

If automated tests are configured:

```bash
pytest
```

Otherwise, follow the project's documented manual test procedure and record the results.

## 🔐 Security

- Never commit `.env` files, private agent seeds, passwords, or API keys.
- Use least-privilege database credentials.
- Keep sensitive credentials out of logs and public documentation.
- Do not publish private beneficiary information.
- Validate user input and handle external service failures safely.

## 📊 Data Disclaimer

Ration Seva must distinguish between demonstration records, user-reported records, and information from verified external sources.

If sample data is used, it must be labelled as sample data and must not be represented as live government PDS information.

Stock reports may be outdated, incomplete, or inconsistent. Even an arithmetically valid report does not guarantee physical stock availability at a Fair Price Shop.

Beneficiaries should confirm uncertain or outdated information with the relevant shop or authorised source before travelling.

## 🌱 Future Scope

- Multilingual assistance in Kannada, Hindi, and English.
- Integration with reliable official PDS data sources where access is available.
- Verified multi-agent coordination for retrieval, validation, and assistance.
- Improved stock summaries and accessible conversational interactions.
- Shop notices and supporting evidence uploads.
- Accessibility improvements for users with limited digital literacy.

These are future goals unless explicitly implemented and verified.

## 👥 Team

**Team:** Ration Seva  
**Event:** Fetch-A-Thon 3.0  
**Venue:** Presidency University, Bengaluru

| Team member | Role |
|---|---|
| Amulya R | Team Lead |
| Athulya Anil | Project Team |
| Disha R | Project Team |
| Reshma | Project Team |

## 🏆 Our Vision

We want to make essential ration information simpler, more transparent, and more useful for the people who depend on it.

Ration Seva connects conversational AI with stock information and validation to help beneficiaries make better-informed decisions.

**Know Before You Go.**

## 📄 License

A licence has not yet been specified. Add a `LICENSE` file and update this section once the team chooses a licence. Do not claim an open-source licence before it has been committed to the repository.
