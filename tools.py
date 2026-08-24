import pandas as pd

from langchain.tools import tool

from config import tickets_file, policies_file



# LOAD CSV DATA


def load_tickets():
    """Load customer tickets from tickets.csv."""
    return pd.read_csv(tickets_file)


def load_policies():
    """Load support policies from policies.csv."""
    return pd.read_csv(policies_file)



# TICKET LOOKUP TOOL


@tool
def get_ticket(ticket_id: str) -> str:
    """
    Look up a customer ticket using its ticket ID.
    Returns the customer's name, email, and message.
    """

    tickets = load_tickets()

    ticket = tickets[
        tickets["ticket_id"].astype(str).str.upper()
        == ticket_id.upper()
    ]

    if ticket.empty:
        return f"No ticket found for {ticket_id}."

    row = ticket.iloc[0]

    return (
        f"Ticket ID: {row['ticket_id']}\n"
        f"Customer Name: {row['customer_name']}\n"
        f"Customer Email: {row['customer_email']}\n"
        f"Customer Message: {row['customer_message']}"
    )



# POLICY SEARCH TOOL


@tool
def search_policy(category: str) -> str:
    """
    Search policies.csv for the policy matching a category.
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
        return f"No policy found for category: {category}"

    results = []

    for _, row in matches.iterrows():

        results.append(
            f"Policy ID: {row['policy_id']}\n"
            f"Category: {row['category']}\n"
            f"Policy Title: {row['policy_title']}\n"
            f"Policy Text: {row['policy_text']}"
        )

    return "\n\n".join(results)


# ALL POLICIES TOOL


@tool
def get_all_policies() -> str:
    """
    Return all policies from policies.csv.
    Useful when the category is unclear.
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

    return "\n\n".join(results)