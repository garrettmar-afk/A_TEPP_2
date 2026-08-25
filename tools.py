import pandas as pd

from langchain.tools import tool

from config import tickets_file, policies_file, LOG_FILE



# LOAD CSV DATA

def load_tickets():
    """Load customer tickets."""
    return pd.read_csv(tickets_file)


def load_policies():
    """Load support policies."""
    return pd.read_csv(policies_file)



# LOGGING


def log_tool_call(tool_name, arguments, result):
    """
    Log every tool call, its arguments,
    and the returned result.
    """

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write("\n" + "=" * 60 + "\n")
        file.write(f"Tool: {tool_name}\n")
        file.write(f"Arguments: {arguments}\n")
        file.write(f"Result:\n{result}\n")



# TICKET LOOKUP TOOL


@tool
def get_ticket(ticket_id: str) -> str:
    """
    Look up a customer ticket.
    """

    tickets = load_tickets()

    ticket = tickets[
        tickets["ticket_id"].astype(str).str.upper()
        == ticket_id.upper()
    ]

    if ticket.empty:

        result = f"No ticket found for {ticket_id}."

        log_tool_call(
            "get_ticket",
            {"ticket_id": ticket_id},
            result
        )

        return result

    row = ticket.iloc[0]

    result = (
        f"Ticket ID: {row['ticket_id']}\n"
        f"Customer Name: {row['customer_name']}\n"
        f"Customer Email: {row['customer_email']}\n"
        f"Customer Message: {row['customer_message']}"
    )

    log_tool_call(
        "get_ticket",
        {"ticket_id": ticket_id},
        result
    )

    return result



# POLICY SEARCH TOOL


@tool
def search_policy(category: str) -> str:
    """
    Search policies.csv for the matching category.
    """

    policies = load_policies()

    matches = policies[
        policies["category"]
        .astype(str)
        .str.lower()
        .str.strip()
        == category.lower().strip()
    ]

    if matches.empty:

        result = f"No policy found for category: {category}"

        log_tool_call(
            "search_policy",
            {"category": category},
            result
        )

        return result

    results = []

    for _, row in matches.iterrows():

        results.append(
            f"Policy ID: {row['policy_id']}\n"
            f"Category: {row['category']}\n"
            f"Policy Title: {row['policy_title']}\n"
            f"Policy Text: {row['policy_text']}"
        )

    result = "\n\n".join(results)

    log_tool_call(
        "search_policy",
        {"category": category},
        result
    )

    return result



# ALL POLICIES TOOL

@tool
def get_all_policies() -> str:
    """
    Return all policies.
    """

    policies = load_policies()

    results = []

    for _, row in policies.iterrows():

        results.append(
            f"Policy ID: {row['policy_id']}\n"
            f"Category: {row['category']}\n"
            f"Policy Title: {row['policy_title']}\n"
            f"Policy Text: {row['policy_text']}"
        )

    result = "\n\n".join(results)

    log_tool_call(
        "get_all_policies",
        {},
        result
    )

    return result
   
        

    
            
