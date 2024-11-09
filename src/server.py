import os

from langchain_core.prompts import ChatPromptTemplate
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain.agents import AgentExecutor

from langchain_openai import ChatOpenAI

import src.utils as u
import constants as c

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

model = u.get_llm_model()

a3_data_agent = create_csv_agent(
    model,
    c.CSV_FILES,
    agent_type=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    allow_dangerous_code=True,
    handle_parsing_errors=True
)

response = a3_data_agent.invoke('Top books by year. limit year 2022')
print(response)
