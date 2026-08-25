# %pip install langchain langchain_deepseek

import os
from pathlib import Path
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_deepseek import ChatDeepSeek

load_dotenv()

data_path = Path("/Users/garrettmar/Desktop/Final TEPP2/A_TEPP_2")
tickets_file = data_path / "tickets.csv"
policies_file = data_path / "policies.csv"
LOG_FILE = data_path / "tool_log.txt"

llm = ChatDeepSeek(
    model="deepseek-v4-flash",
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    temperature=0
)
