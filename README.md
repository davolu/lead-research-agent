# Lead Research Agent (Langflow)

Type a company name, get a short research brief back, and add one row to a CSV file.

Built for the video "Let's Build an AI Lead Research Agent in Langflow".

## What's inside

| File | What it is |
| --- | --- |
| `lead-research-agent.json` | The Langflow flow. Import it in Langflow. |
| `predict.py` | Calls the flow from Python through the Langflow API. |
| `sample-output/leads-header.csv` | The CSV columns the flow writes. |
| `.env.example` | The settings `predict.py` reads. Copy to `.env` and fill in. |

## The flow

```
Chat Input ──► Agent ──► Parser ──► Chat Output        (brief in the Playground)
                ▲   │
Anthropic ──────┘   └──► Type Convert (Table) ──► Write File (leads.csv, Append on)
  (claude-haiku-5-5)
Web Search (tool) ─► Agent
```

- **Model:** the **Anthropic** component, with model name `claude-haiku-5-5` typed in (it is a combobox, so a name that is not in the dropdown still works). The API key is loaded from a Langflow global variable named `ANTHROPIC_API_KEY`.
- **Search:** Langflow's built-in **Web Search** component in tool mode. Web mode uses DuckDuckGo, News mode uses Google News. No search key needed.
- **Output:** the Agent's **Structured Response** with seven fields: `date, company, what_it_does, size_signals, recent_news, outreach_angle, sources`.
- **Saving:** **Write File** with format `csv` and **Append** switched on, so every company adds a row.

## Setup

Tested with **Langflow 1.13.4** on Python 3.12.

```bash
uv pip install langflow==1.13.4
export LANGFLOW_SUPERUSER=langflow
export LANGFLOW_SUPERUSER_PASSWORD='choose-a-password'
# optional: load the model key into a Langflow global variable on startup
export LANGFLOW_VARIABLES_TO_GET_FROM_ENVIRONMENT=ANTHROPIC_API_KEY
uv run langflow run
```

Langflow 1.13 turned auto-login off, so you sign in with the superuser you set above.
Open http://127.0.0.1:7860.

1. Get an Anthropic API key at https://console.anthropic.com/.
2. In Langflow, **Settings → Global Variables**, add `ANTHROPIC_API_KEY` with your key (type Credential), unless you already exported it as shown above.
3. **Upload** `lead-research-agent.json` on the Projects page.
4. Open **Playground**, type a company name, e.g. `Stripe`.

Write File saves `leads.csv` inside Langflow's own storage folder for your user. Its **File Path** output shows where. The file name field accepts a name only, not a path.

## Model cost (from a real run)

On 25 Nov 2026 we ran three public companies (Stripe, Shopify, Notion) through this flow on `claude-haiku-5-5`.
Langflow reported **24,471 input tokens** and **4,778 output tokens** in total (Stripe 8,740 / 1,755; Shopify 7,256 / 1,731; Notion 8,475 / 1,292).
At Anthropic's published prices that day for Haiku 5.5, for prompts under 100,000 tokens — **$0.10 per million input tokens and $0.50 per million output tokens** — that comes to **$0.0048**.
Prices are listed at https://platform.claude.com/docs/en/about-claude/pricing and can change.

## Call it from Python

```bash
pip install requests
cp .env.example .env    # fill in the three values, then load them into your shell
python predict.py "Stripe"
```

Create the API key under **Settings → Langflow API Keys**. Copy the flow ID from **Share → API access**.

Use a fresh `session_id` for each company so earlier briefs are not mixed in. `predict.py` already does this.

## Rules worth keeping

- Use **public company names only**. Don't type personal details about people.
- The prompt tells the agent never to invent numbers or news, and to write "Not found in sources" instead. Still check the sources before you use a brief.
- If DuckDuckGo rate-limits your network, Web mode comes back empty. The agent should say so and lean on News results. On 25 Nov 2026, DuckDuckGo returned HTTP 202 from the machine that built this, so the demo briefs used news headlines and no source URLs.
