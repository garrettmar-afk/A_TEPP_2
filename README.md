Multi-Agent Customer Support System

A multi-agent system built with LangChain, DeepSeek, and Pandas to help automate customer support tickets. This project handles ticket triage, policy lookups, and draft generation using specialized LLM agents coordinated by a main orchestrator, with an exception-based human review process.

---

 Architecture & Workflow

```
                        Customer Ticket
                               │
                               ▼
                   ┌──────────────────────┐
                   │     Orchestrator     │
                   │ Routes & Coordinates │
                   └──────────┬───────────┘
                               │
              ┌────────────────┴──────────────┐
              ▼                               ▼
      Triage Agent                       Policy Agent
 (Categorize & Flag)               (Retrieve Policy & Draft)
              │                               │
              └───────────────┬───────────────┘
                              ▼
                     Shared Ticket State
            (Category, Flag Status, Draft Reply)
                              │
                              ▼
                     Reviewer / Critic Agent
                  (Checks policy & response)
                              │
                   ┌──────────┴──────────┐
                   ▼                     ▼
          Flagged / Failed            Approved
                   │                     │
                   ▼                     ▼
          Human Supervisor         Auto Response

```

### Key Highlights

* Orchestrator Pattern: A central engine (`orchestrator.py`) routes tasks and manages state between different agents.


* Specialized Agents: Each agent uses its own prompt to focus on a specific task (Triage, Policy, or Reviewer).


* Shared State: A shared dictionary tracks ticket details, categories, flag statuses, and draft replies throughout the pipeline.


* Exception-Only Approval Gate: Routine tickets are answered automatically, while complex or flagged tickets are sent to a human supervisor.



---

Before vs. After Comparison

| Workflow Step | Manual Workflow | Multi-Agent Workflow |
| --- | --- | --- |
| Initial Triage | Read and tagged manually by staff | Categorized and flagged in seconds by `triage_agent`<br> |
| Policy Search| Searching internal docs manually | Looking up exact rules directly via `policies.csv` using tools

 |
| Quality Check| Inconsistent tones/accuracy across team | Double-checked against policies by `reviewer_agent`<br> |
| Human Effort| Staff handles 100% of incoming tickets | Staff only steps in for flagged or tricky tickets

 |

---

 Project Structure

```
├── config.py         # App configs, model settings, and file paths
├── tools.py          # Data retrieval tools (Pandas) and logging
├── subagents.py      # Agent setup and system prompts
├── agent.py          # Functions to interact with agents
├── orchestrator.py   # Main pipeline control and decision logic
├── main.py           # CLI entry point to run the project
├── tickets.csv       # Sample customer tickets dataset
├── policies.csv      # Company policy rules dataset
└── tool_log.txt      # Execution log generated during runs

```

---

 File Breakdown

### `config.py`

Holds configuration settings in one place. Defines file paths (`tickets.csv`, `policies.csv`, `tool_log.txt`) and sets up the DeepSeek model used by the agents.

### `tools.py`

Contains the Python functions that let agents fetch real data from CSV files instead of relying on memory. Every tool usage is logged to `tool_log.txt`.

* `get_ticket(ticket_id)`: Fetches ticket details by ID.


* `search_policy(category)`: Pulls relevant policy info based on category.


* `get_all_policies()`: Backup tool to pull all policies if category is unclear.



### `subagents.py`

Defines the three AI sub-agents and their individual system prompts:

* Triage Agent: Reads the ticket, assigns a category (Returns, Billing, or Technical), and decides if it needs human review.


* Policy Agent: Fetches the right policies and writes a initial customer response draft.


* Reviewer / Critic Agent: Double-checks the draft for accuracy, policy adherence, and safety.



### `agent.py`

Serves as a bridge between `orchestrator.py` and `subagents.py` by providing simple wrapper functions (`ask_triage_agent`, `ask_policy_agent`, `ask_reviewer`).

### `orchestrator.py`

Runs the main execution flow:

1. Creates a shared state dictionary.


2. Sends the ticket to the Triage Agent. If flagged, sends it straight to human review.


3. Otherwise, sends it to the Policy Agent to generate a response.


4. Passes the draft to the Reviewer Agent. Retries the Policy Agent once if rejected.



### `main.py`

The entry point script. Loads tickets from `tickets.csv`, prompts the user to pick a ticket ID (or run all), executes `process_ticket()`, and outputs the final results while saving tool execution logs.

---

## 🚀 How to Run

1. **Clone the repo:**
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name

```


2. **Install dependencies:**
```bash
pip install langchain pandas

```


3. **Set API key:**
```bash
export DEEPSEEK_API_KEY="your_api_key_here"

```


4. **Run the app:**
```bash
python main.py

```
