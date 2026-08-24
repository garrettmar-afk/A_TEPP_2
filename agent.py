
from langchain.tools import tool

from subagents import (
    triage_agent,
    policy_agent,
    reviewer_agent
)




def run_agent(agent, prompt):
    """
    Send a prompt to a LangChain agent
    and return its final response.
    """

    result = agent.invoke({
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    return result["messages"][-1].content




@tool
def ask_triage_agent(ticket: str) -> str:
    """
    Ask the Triage Agent to classify a customer support ticket.
    """

    print("\n[orchestrator] -> triage_agent")

    result = run_agent(
        triage_agent,
        ticket
    )

    print("[triage_agent] -> orchestrator")
    print(result)

    return result




@tool
def ask_policy_agent(ticket_information: str) -> str:
    """
    Ask the Policy Agent to find the correct policy
    and create a customer response.
    """

    print("\n[orchestrator] -> policy_agent")

    result = run_agent(
        policy_agent,
        ticket_information
    )

    print("[policy_agent] -> orchestrator")
    print(result)

    return result




@tool
def ask_reviewer(review_information: str) -> str:
    """
    Ask the Reviewer Agent to check the proposed response.
    """

    print("\n[orchestrator] -> reviewer")

    result = run_agent(
        reviewer_agent,
        review_information
    )

    print("[reviewer] -> orchestrator")
    print(result)

    return result