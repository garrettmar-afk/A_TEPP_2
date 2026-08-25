# critic_agent.py

# 1️ Import libraries
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv

#  Logging counters
pass_count = 0
fail_count = 0


# 2️ Load environment variables
load_dotenv()

# 3️ Using DeepSeek Flash v4 (API model name: deepseek-chat)
llm = ChatOpenAI(
    openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
    openai_api_base="https://api.deepseek.com",
    model="deepseek-chat", # Flash v4
    temperature=0.3
)

# 4️ Define your critic prompt
critic_prompt = PromptTemplate(
    input_variables=["triage_text"],
    template="""
    You are the QA Critic Agent. Evaluate the following triage message:

    {triage_text}

    Evaluate the triage for:
    - Accuracy (does it correctly address the ticket intent?)
    - Clarity (is the response detailed and actionable?)
    - Professionalism (is it polite and avoids vague or dismissive language?)

    Score it PASS or FAIL based on these criteria.
    If FAIL, rewrite it and explain why.
    """
)

def evaluate_triage(triage_text):
    return critic_chain.invoke({"triage_text": triage_text})



# 5️ Create the LangChain pipeline
critic_chain = critic_prompt | llm | StrOutputParser()

# 6️ Example test run
def evaluate_ticket(ticket, triage_output):
    global pass_count, fail_count
    result = critic_chain.invoke({"ticket": ticket, "triage_output": triage_output})
    print("Critic Result:\n", result)

    if "FAIL" in result:
        fail_count += 1
        retry_triage(ticket, triage_output)
    else:
        pass_count += 1

    print(f"Summary → PASS: {pass_count} | FAIL: {fail_count}")


def retry_triage(ticket, triage_output):
    print("Retry triggered: sending back to triage agent for correction...")
    feedback_prompt = (
        f"The critic marked this triage as FAIL.\n"
        f"Ticket: {ticket}\n"
        f"Triage Output: {triage_output}\n"
        "Revise the triage to fix accuracy, clarity, or safety issues."
    )
    revised_output = llm.invoke(feedback_prompt)
    print("Revised Triage:\n", revised_output.content)
    return revised_output


if __name__ == "__main__":
    sample_ticket = "Customer reports that their login credentials are not working."
    sample_output = "Tell them to try again later."
    evaluate_ticket(sample_ticket, sample_output)
