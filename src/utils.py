import os

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
# from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_cohere import create_csv_agent

from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

load_dotenv()


def get_llm_model():
    model_openai = ChatOpenAI(
        temperature=0.2, model='gpt-4o', openai_api_key=OPENAI_API_KEY
    )

    return model_openai


prompt = ChatPromptTemplate.from_messages(
    [
        (
            'system',
            """You are a helpull assistant that can help me with my book search. Your name is BA3s.\n
         You have access to these csv: {documents} Thought:{agent_scratchpad}""",
        ),
        ('human', '{input}'),
    ]
)


# TODO: Implement flags to choose between different create_csv_agent
# def get_agent(path):
#     return create_csv_agent(
#         get_llm_model(),
#         path=path,
#         agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#         verbose=True,
#         allow_dangerous_code=True,
#         handle_parsing_errors=True,
#     )


BASE_PROMPT = """
You are a specialist in data analysis. Your name is BA3s. Always greet the user and ask how you can help them.
You are working with multiple pandas dataframes in Python named df1, df2, etc.
You should use the tools below to answer the question posed of you:\n\nipython - A Python shell. 
Use this to execute python commands. Input should be a valid python command.
When using this tool, sometimes output is abbreviated - make sure it does not look abbreviated before using it in your answer.

Use the following format:\n\nQuestion: the input question you must answer\n
Thought: you should always think about what to do\n
Action: the action to take, should be one of [python_repl_ast]\n
Action Input: the input to the action\nObservation: the result of the action\n... (this Thought/Action/Action Input/Observation can repeat N times)\n
Thought: I now know the final answer\nFinal Answer: the final answer to the original input question\n\n\n
This is the result of `print(df.head())` for each dataframe

If you got  asked to plot graphs and charts, think step by step. and use Action Input generated code
Remember to remove the special characters r"```python(.*?)```" from the code obtained on Action Input before running it.
You'll plot it on streamlit, so you need to uso st.pyplot() to show the plot.
"""
agent_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', BASE_PROMPT),
        ('human', '{input}'),
        MessagesPlaceholder('agent_scratchpad'),
    ]
)


def get_agent_with_prompt(path):
    return create_csv_agent(
        get_llm_model(),
        path=path,
        # prompt=agent_prompt,
        # agent_type=AgentType.OPENAI_FUNCTIONS,
        # verbose=True,
        # allow_dangerous_code=True,
        # handle_parsing_errors=True,
    )


class MessagePayload(BaseModel):
    """MessagePayload class to handle the input from the user"""

    input: str
    output: str
