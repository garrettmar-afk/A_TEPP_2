import re

from tools import get_ticket
from agent import (
    ask_triage_agent,
    ask_policy_agent,
    ask_reviewer
)



# SHARED STATE

def create_shared_state(ticket_data):

    return {
        "ticket_id": ticket_data["ticket_id"],
        "customer_name": ticket_data["customer_name"],
        "customer_email": ticket_data["customer_email"],
        "customer_message": ticket_data["customer_message"],

        "category": "",
        "flagged": False,

        "policy_title": "",
        "policy_text": "",

        "draft_response": "",

        "review_status": "",
        "review_reason": "",

        "final_response": "",

        "logs": []
    }



# LOGGING

def add_log(state, agent_name, input_text, output_text):

    state["logs"].append({
        "agent": agent_name,
        "input": input_text,
        "output": output_text
    })



# CONVERT TICKET TEXT INTO DATA

def parse_ticket(ticket_text):

    ticket_id = re.search(
        r"Ticket ID:\s*(.+)",
        ticket_text,
        re.IGNORECASE
    )

    customer_name = re.search(
        r"Customer Name:\s*(.+)",
        ticket_text,
        re.IGNORECASE
    )

    customer_email = re.search(
        r"Customer Email:\s*(.+)",
        ticket_text,
        re.IGNORECASE
    )

    customer_message = re.search(
        r"Customer Message:\s*(.+)",
        ticket_text,
        re.IGNORECASE
    )

    return {
        "ticket_id": ticket_id.group(1).strip()
        if ticket_id else "",

        "customer_name": customer_name.group(1).strip()
        if customer_name else "",

        "customer_email": customer_email.group(1).strip()
        if customer_email else "",

        "customer_message": customer_message.group(1).strip()
        if customer_message else ""
    }



# EXTRACT CATEGORY

def extract_category(triage_result):

    match = re.search(
        r"CATEGORY:\s*(.+)",
        triage_result,
        re.IGNORECASE
    )

    if match:
        return match.group(1).strip()

    return "Unknown"



# EXTRACT FLAG

def extract_flag(triage_result):

    match = re.search(
        r"FLAGGED:\s*(YES|NO)",
        triage_result,
        re.IGNORECASE
    )

    if match:
        return match.group(1).upper() == "YES"

    return True



# EXTRACT REVIEW DECISION

def extract_review_decision(review_result):

    match = re.search(
        r"DECISION:\s*(APPROVED|REJECTED)",
        review_result,
        re.IGNORECASE
    )

    if match:
        return match.group(1).upper()

    return "REJECTED"



# PROCESS ONE TICKET

def process_ticket(ticket_id):

    print("\n" + "=" * 70)
    print(f"PROCESSING TICKET: {ticket_id}")
    print("=" * 70)


    
    # STEP 1: GET TICKET


    ticket_result = get_ticket.invoke({
        "ticket_id": ticket_id
    })

    ticket_data = parse_ticket(ticket_result)

    state = create_shared_state(ticket_data)


    
    # STEP 2: TRIAGE AGENT
    

    triage_prompt = f"""
Customer Ticket

Ticket ID: {state["ticket_id"]}

Customer: {state["customer_name"]}

Message:
{state["customer_message"]}

Classify this ticket.
"""

    triage_result = ask_triage_agent.invoke({
        "ticket": triage_prompt
    })

    add_log(
        state,
        "Triage Agent",
        triage_prompt,
        triage_result
    )

    state["category"] = extract_category(
        triage_result
    )

    state["flagged"] = extract_flag(
        triage_result
    )

    print("\nCATEGORY:", state["category"])
    print("FLAGGED:", state["flagged"])


    
    # STEP 3: IF TRIAGE FLAGS THE TICKET
    
    if state["flagged"]:

        state["review_status"] = "Human Review Required"

        state["final_response"] = (
            "This ticket requires review by a human supervisor."
        )

        print("\nRESULT: FLAGGED FOR HUMAN REVIEW")

        return state


    
    # STEP 4: POLICY AGENT
    

    policy_prompt = f"""
Customer Support Ticket

Ticket ID:
{state["ticket_id"]}

Customer:
{state["customer_name"]}

Customer Message:
{state["customer_message"]}

Triage Category:
{state["category"]}

Find the correct policy and create a customer response.
Use the policy tools.
"""

    policy_result = ask_policy_agent.invoke({
        "ticket_information": policy_prompt
    })

    add_log(
        state,
        "Policy Agent",
        policy_prompt,
        policy_result
    )

    state["draft_response"] = policy_result


    
    # STEP 5: REVIEWER
    

    review_prompt = f"""
Review this customer support response.

CUSTOMER MESSAGE:
{state["customer_message"]}

CATEGORY:
{state["category"]}

PROPOSED RESPONSE:
{state["draft_response"]}

Check whether the response follows the policy
and correctly addresses the customer's issue.
"""

    review_result = ask_reviewer.invoke({
        "review_information": review_prompt
    })

    add_log(
        state,
        "Reviewer",
        review_prompt,
        review_result
    )

    decision = extract_review_decision(
        review_result
    )

    state["review_status"] = decision
    state["review_reason"] = review_result


    
    # STEP 6: APPROVED
    

    if decision == "APPROVED":

        state["final_response"] = (
            state["draft_response"]
        )

        print("\nRESULT: APPROVED")

        print("\nAUTOMATIC RESPONSE:")
        print(state["final_response"])

        return state


    
    # STEP 7: RETRY POLICY AGENT
    

    print("\nReviewer rejected response.")
    print("Retrying Policy Agent...")

    retry_prompt = f"""
The previous response was rejected by the reviewer.

Customer message:
{state["customer_message"]}

Category:
{state["category"]}

Previous response:
{state["draft_response"]}

Reviewer feedback:
{review_result}

Create a corrected response.

Use the policy information.
Do not invent information.
"""

    retry_result = ask_policy_agent.invoke({
        "ticket_information": retry_prompt
    })

    add_log(
        state,
        "Policy Agent - Retry",
        retry_prompt,
        retry_result
    )

    state["draft_response"] = retry_result


    
    # STEP 8: REVIEW RETRY
    

    retry_review_prompt = f"""
Review the corrected response.

Customer message:
{state["customer_message"]}

Category:
{state["category"]}

Corrected response:
{state["draft_response"]}

Determine whether it is safe and correct to send.
"""

    retry_review_result = ask_reviewer.invoke({
        "review_information": retry_review_prompt
    })

    add_log(
        state,
        "Reviewer - Retry",
        retry_review_prompt,
        retry_review_result
    )

    retry_decision = extract_review_decision(
        retry_review_result
    )


    
    # STEP 9: FINAL DECISION
    

    if retry_decision == "APPROVED":

        state["review_status"] = (
            "Approved After Retry"
        )

        state["final_response"] = (
            state["draft_response"]
        )

        print("\nRESULT: APPROVED AFTER RETRY")

        print("\nAUTOMATIC RESPONSE:")
        print(state["final_response"])

    else:

        state["review_status"] = (
            "Human Review Required"
        )

        state["final_response"] = (
            "This ticket requires review by a human supervisor."
        )

        print("\nRESULT: FLAGGED FOR HUMAN REVIEW")


    return state