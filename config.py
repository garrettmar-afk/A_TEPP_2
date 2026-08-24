# %pip install langchain langchain_deepseek

import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_deepseek import ChatDeepSeek

load_dotenv()
data_path = path(r".....")
tickets_file = data_path / "tickets.csv"
policies_file = data_path / "policies.csv"

llm = ChatDeepSeek(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0
)
