# Northstar Support — Multi-Agent Ticket Triage

**TEPP Phase 2 — Northstars Team**
Replaces the manual triage-and-route step at Northstar Support Co. with an
Orchestrator/Subagent architecture, using a Reviewer/Critic agent as an
exception-based stand-in for the supervisor's second look.

## Fixes in this fork

This fork corrects a few bugs found while getting the project running locally:

- **`config.py`** — `data_path` used an undefined `path()` function and a placeholder
  string instead of `Path(...)`; also, `LOG_FILE` was referenced in `tools.py` but never
  defined in `config.py`. Both are now fixed.
- **`requirements.txt`** — added `pandas`, which `tools.py` and `main.py` import but
  which was missing from the pinned dependency list.
- **`.gitignore`** — added `.env`, `__pycache__/`, `venv/`, and `tool_log.txt`. `.env`
  in particular was not previously excluded, meaning API keys could have been committed
  by accident.
- Added `Northstar_Code_Reference.docx` — a line-by-line reference doc for every file
  in the project.
- Added `README.md` itself — the original repo had no README. This one documents how
  the pipeline works, what each file does, setup/run instructions, and the team roster.

## How it works

A ticket goes through three specialist agents, coordinated by
`orchestrator.py`:

1. **Triage Agent** classifies the ticket (Returns / Billing / Technical)
   and flags it for human review if it's unclear, high-risk, or outside
   those categories.
2. **Policy Agent** looks up the matching policy in `policies.csv` and
   drafts a customer response grounded in it.
3. **Reviewer Agent** checks the draft against the policy and either
   approves it or rejects it with feedback.

If the Reviewer rejects a draft, the Policy Agent gets one retry with the
reviewer's feedback attached. If it's still rejected after the retry, or
if Triage flagged the ticket up front, the ticket is marked
`"Human Review Required"` instead of being sent automatically — that's
the human checkpoint this system preserves.

Every tool call (ticket lookups and policy searches) is also written out
to `tool_log.txt` via `log_tool_call()` in `tools.py`, capturing the tool
name, its arguments, and its result — the audit trail for the demo.

## Files

| File | What it does |
|---|---|
| `config.py` | Loads `.env`, builds the shared DeepSeek (`llm`) client, points to the CSV data files and the tool-call log file (`LOG_FILE`) |
| `tools.py` | `get_ticket`, `search_policy`, `get_all_policies` — `@tool` functions backed by `policies.csv` / `tickets.csv` via pandas, plus `log_tool_call()` which writes every tool call to `tool_log.txt` |
| `subagents.py` | Builds the three agents (`triage_agent`, `policy_agent`, `reviewer_agent`) with `create_agent()` |
| `agent.py` | Wraps each subagent as a callable tool (`ask_triage_agent`, `ask_policy_agent`, `ask_reviewer`) |
| `orchestrator.py` | `process_ticket(ticket_id)` — the actual pipeline: pulls the ticket, runs it through triage → policy → review, handles the retry logic, and returns the final state (including the full agent-by-agent log) |
| `main.py` | **Entry point.** Clears `tool_log.txt`, lists all available tickets, then prompts you to enter a ticket ID (or `ALL`) and runs it/them through `process_ticket()`, printing the full result |
| `policies.csv` | Northstar's support policies, by category |
| `tickets.csv` | Sample customer tickets |
| `requirements.txt` | Pinned dependencies |

## Setup

1. Create a `.env` file in this folder with your DeepSeek key:
   ```
   DEEPSEEK_API_KEY=your_key_here
   ```
2. Create and activate a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running it

```bash
python main.py
```

This will:
1. Clear and start a fresh `tool_log.txt`
2. Print a table of every ticket in `tickets.csv`
3. Prompt you: `Enter a ticket ID or type ALL:`
   - Enter a specific ID (e.g. `T001`) to run just that ticket and see
     its full result — category, flagged status, policy used, draft
     response, review status/reason, and final response.
   - Enter `ALL` to run every ticket and get a short summary table
     (ticket ID, category, review status) at the end.

## Team

- **Prompt Engineer:** Garrett — system prompts for Triage, Policy, and Reviewer agents
- **Orchestrator Engineer:** Shweta — routing/coordination logic
- **Integration Engineer:** Marlayshia — data ingestion, agent wiring
- **QA / Critic Engineer:** Alexis — reviewer logic, retry loop
- **Logging & Observability Engineer:** Emmanuel — `tool_log.txt` and the `logs` trail on each ticket's state
