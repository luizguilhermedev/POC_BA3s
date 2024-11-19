import os

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


from dotenv import load_dotenv

from src.prompts import instruct_prompt

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

db = SQLDatabase.from_uri("sqlite:///books.db")

model = ChatGroq(
    model='llama-3.1-8b-instant',
    api_key=GROQ_API_KEY,
    max_tokens=1000,
)

toolkit = SQLDatabaseToolkit(db=db, llm=model)


agent_executor = create_sql_agent(
    model,
    toolkit=toolkit,
    prompt=instruct_prompt,
    # db=db,
    agent_type="openai-tools",
    verbose=True)

response = agent_executor.stream({"input": "", "chat_history": []})

for chunk in response:
    print(chunk.get('output'))




