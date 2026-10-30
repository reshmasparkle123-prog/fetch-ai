# RationSeva Shortage Analyst (internal agent)

> **This is an internal agent.** It is called by the **RationSeva Coordinator**, the public ASI:One chat agent, and does not speak the chat protocol. To use RationSeva, chat with the Coordinator: `agent1q0gvf0grxdvpqzg4t4s55p5du4y97daurpd99sq40xc8en4qmkrvga9a2fv`.

## What it does

It receives a shop's validated stock from the Coordinator. The stock comes from the Stock Validator, which reads the AP AePDS public report snapshot of 2026-10-20 22:00 for 480 fair-price shops in Alluri Sitharama Raju district. The analyst then:

1. **Classifies each item**, using the same rule as the data pipeline:
   - **LOW**: closing stock under **10%** of this month's available stock (closing + issued)
   - **OUT_OF_STOCK**: closing stock ≤ 0.01
   - otherwise **AVAILABLE**
2. **Answers "Where else can I go?"** For a LOW or OUT item, or any item the user asks about, it returns up to **3 other shops in the same AFSO** that have that item **AVAILABLE**, largest stock first.

It never invents stock. Empty-sack entries ("10KG BAG", "15KG BAG") are excluded because they aren't ration.

## Protocol

| Direction | Model | Key fields |
|---|---|---|
| in | `ShortageRequest` | `fps_id`, `afso`, `commodities[]` (closing, received, issued, unit), `commodity_requested`, `want_alternatives` |
| out | `ShortageAnalysis` | `assessments[]` (status, percent_left), `alternatives{commodity: [shop…]}`, `data_time`, `analysis` |

Schemas: [`messages.py`](https://github.com/reshmasparkle123-prog/fetch-ai/blob/asad/real-data-agents/messages.py)

## Example

Shop 0306122, Rice: 9.35 kg left of 6,899.35 kg this month → **LOW (0.1%)**.
Alternatives in Ananthagiri AFSO: **0306133** (2,318.90 kg), **0306127** (1,498.85 kg), **0306128** (1,425.80 kg).

_Data is a dated snapshot, not live._

Source: <https://github.com/reshmasparkle123-prog/fetch-ai> (branch `asad/real-data-agents`)
