import os
import re
from pathlib import Path
from typing import Union, Callable, Any

import pandas as pd
from fastapi import HTTPException
from langchain_community.chat_message_histories import (
    FileChatMessageHistory,
    PostgresChatMessageHistory,
)
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceBgeEmbeddings
from langchain_core.chat_history import (
    InMemoryChatMessageHistory,
    BaseChatMessageHistory,
)
from langchain_core.runnables import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits.csv.base import create_csv_agent
# from langchain_cohere import create_csv_agent

import streamlit as st
from matplotlib import pyplot as plt

from pydantic import BaseModel, Field

from dotenv import load_dotenv

from src.constants import PATH_TO_FILE

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

AM_API_KEY = os.getenv('AM_API_KEY')

load_dotenv()


def get_llm_model(use_openai: bool = True):
    if use_openai:
        model_openai = ChatOpenAI(
            temperature=0.2, model='gpt-4o', openai_api_key=OPENAI_API_KEY
        )

        return model_openai

    amazonia = ChatOpenAI(
        api_key=AM_API_KEY,
        model='amazonia-1-biofy-tuned',
        temperature=0.4,
        max_tokens=1500,
        base_url='https://api.amazoniaia.com.br/v1',
    )

    return amazonia


def get_agent(path: list[str]):
    return create_csv_agent(
        get_llm_model(use_openai=False),
        path=path,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        allow_dangerous_code=True,
    )


def get_embedding_model():
    embeddings = HuggingFaceBgeEmbeddings(
        model_name='BAAI/bge-m3',
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True},
        show_progress=True,
    )
    return embeddings


def get_retriever():
    vector_store = Chroma(
        embedding_function=get_embedding_model(),
        persist_directory='vectordb_data/',
    )

    return vector_store.as_retriever()


def _is_valid_identifier(value: str) -> bool:
    """Check if the value is a valid identifier."""
    # Use a regular expression to match the allowed characters
    valid_characters = re.compile(r'^[a-zA-Z0-9-_]+$')
    return bool(valid_characters.match(value))


def create_session_factory(
    base_dir: Union[str, Path],
) -> Callable[[str], BaseChatMessageHistory]:
    """Create a session ID factory that creates session IDs from a base dir.

    Args:
        base_dir: Base directory to use for storing the chat histories.

    Returns:
        A session ID factory that creates session IDs from a base path.
    """
    base_dir_ = Path(base_dir) if isinstance(base_dir, str) else base_dir
    if not base_dir_.exists():
        base_dir_.mkdir(parents=True)

    def get_chat_history(session_id: str) -> FileChatMessageHistory:
        """Get a chat history from a session ID."""
        if not _is_valid_identifier(session_id):
            raise HTTPException(
                status_code=400,
                detail=f'Session ID `{session_id}` is not in a valid format. '
                'Session ID must only contain alphanumeric characters, '
                'hyphens, and underscores.',
            )
        file_path = base_dir_ / f'{session_id}.json'
        return FileChatMessageHistory(str(file_path))

    return get_chat_history


def conversational_chain(path: list[str] = PATH_TO_FILE):
    chain_with_history = RunnableWithMessageHistory(
        get_agent(path), create_session_factory('chat_histories'),
        input_messages_key='input'
    ).with_types(input_type=InputChat)

    return chain_with_history


def extract_code_from_response(response):
    """Extracts Python code from a string response.
    Use regex pattern to match content between triple backticks.
    Args:
        response (str): The response string.
    Returns:
        str: The Python code extracted from the response.
    """
    code_pattern = r'```python(.*?)```'
    match = re.search(code_pattern, response, re.DOTALL)

    if match:
        python_code = match.group(1).strip()
        modified_code = re.sub(
            r'dados\s*=\s*\{.*?}',
            'df = df',
            python_code,
            flags=re.DOTALL,
        )
        return modified_code

    return response


def initialize_chatbot_ui(chain):
    st.title('BA3s - v0.1')

    session_id = st.sidebar.text_input('Your Session ID Here')
    config = {'configurable': {'session_id': session_id}}

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.chat_message('ai').write(
        'Olá, sou BA3s, especialista em análise de avaliações de livros. Como posso ajudar você hoje?'
    )

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.markdown(message['content'])

    # Accept user input
    if prompt := st.chat_input('Sua mensagem...'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            prompt = str(prompt)
            response = chain(prompt, config)
            executable_code = extract_code_from_response(response)
            if executable_code:
                st.write(response)
                st.code(executable_code, language='python')
                exec(
                    executable_code,
                    globals(),
                    {'df': pd.DataFrame(), 'plt': plt},
                )
                fig = plt.gcf()  # Get current figure
                st.pyplot(fig)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response}
                )

            else:
                st.write(response)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response}
                )


class InputChat(BaseModel):
    """Input for the chat endpoint."""

    # The field extra defines a chat widget.
    # As of 2024-02-05, this chat widget is not fully supported.
    # It's included in documentation to show how it should be specified, but
    # will not work until the widget is fully supported for history persistence
    # on the backend.
    human_input: str = Field(
        ...,
        description='The human input to the chat system.',
    )


# Pydantic models to be used with FastAAPI
class MessagePayload(BaseModel):
    """MessagePayload class to handle the input from the user"""

    input: str
    output: str
