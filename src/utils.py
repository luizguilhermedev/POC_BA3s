import os

from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent

from pydantic import BaseModel
import src.constants as c

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

load_dotenv()


def get_llm_model():
    model_openai = ChatOpenAI(
        temperature=0.2, model='gpt-4o', openai_api_key=OPENAI_API_KEY
    )

    return model_openai


def get_agent(path):
    return create_csv_agent(
        get_llm_model(),
        path=path,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
    )



# agent = get_agent(c.PATH_TO_FILE)
#
# print(agent.get_graph())
# response = agent.stream({'input': 'datasets you have access to'})
# print(type(response))
# answer = ''
# # Get output key
#
# for chunk in response:
#     answer += chunk
#     print(answer['output'])
# answer = ''
# for chunk in response:
#
#     answer += chunk
#     print(answer)


class MessagePayload(BaseModel):
    """MessagePayload class to handle the input from the user"""
    input: str
    output: str

