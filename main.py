import pandas as pd

from config import tickets_file
from orchestrator import process_ticket
from config import LOG_FILE

# Clear previous tool log
with open(LOG_FILE, "w", encoding="utf-8") as file:
    file.write("TOOL LOG\n")
    file.write("=" * 60 + "\n")


# =========================================================
# LOAD TICKETS
# =========================================================

tickets = pd.read_csv(tickets_file)


# =========================================================
# DISPLAY AVAILABLE TICKETS
# =========================================================

print("=" * 70)
print("CUSTOMER SUPPORT MULTI-AGENT SYSTEM")
print("=" * 70)

print("\nAvailable Tickets:")

print(
    tickets[
        [
            "ticket_id",
            "customer_name",
            "customer_message"
        ]
    ].to_string(index=False)
)


# =========================================================
# ASK USER WHAT TO PROCESS
# =========================================================

ticket_choice = input(
    "\nEnter a ticket ID or type ALL: "
).strip()


# =========================================================
# PROCESS ALL TICKETS
# =========================================================

if ticket_choice.upper() == "ALL":

    all_results = []

    for ticket_id in tickets["ticket_id"]:

        result = process_ticket(
            ticket_id
        )

        all_results.append(result)

    print("\n" + "=" * 70)
    print("FINAL SUMMARY")
    print("=" * 70)

    for result in all_results:

        print(
            f"\nTicket ID: {result['ticket_id']}"
        )

        print(
            f"Category: {result['category']}"
        )

        print(
            f"Review Status: {result['review_status']}"
        )

        print("-" * 70)


# =========================================================
# PROCESS ONE TICKET
# =========================================================

else:

    matching_ticket = tickets[
        tickets["ticket_id"].astype(str).str.upper()
        == ticket_choice.upper()
    ]

    if matching_ticket.empty:

        print(
            f"\nTicket {ticket_choice} was not found."
        )

    else:

        result = process_ticket(
            ticket_choice
        )

        # -------------------------------------------------
        # PRINT SHARED STATE
        # -------------------------------------------------

        print("\n" + "=" * 70)
        print("FINAL SHARED TICKET STATE")
        print("=" * 70)

        print(
            f"\nTicket ID: {result['ticket_id']}"
        )

        print(
            f"Customer Name: {result['customer_name']}"
        )

        print(
            f"Customer Email: {result['customer_email']}"
        )

        print(
            f"Customer Message: {result['customer_message']}"
        )

        print(
            f"\nCategory: {result['category']}"
        )

        print(
            f"Flagged: {result['flagged']}"
        )

        print(
            f"Policy Title: {result['policy_title']}"
        )

        print(
            f"Policy Text: {result['policy_text']}"
        )

        print(
            f"\nDraft Response:\n{result['draft_response']}"
        )

        print(
            f"\nReview Status: {result['review_status']}"
        )

        print(
            f"Review Reason:\n{result['review_reason']}"
        )

        print(
            f"\nFinal Response:\n{result['final_response']}"
        )

        print("\n" + "=" * 70)