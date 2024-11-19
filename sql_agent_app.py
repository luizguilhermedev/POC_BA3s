import io
import os
import sys

from dotenv import load_dotenv
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq

import src.constants as c
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils import conversational_chain, extract_code_from_response
from src.prompts import instruction, instruct_prompt

import streamlit as st

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

# Streamlit UI

st.chat_message('ai').write(
        'Olá, sou BA3s, especialista em análise de avaliações de livros. Como posso ajudar você hoje?'
    )

if 'messages' not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.write(message['content'])

if prompt := st.chat_input('Sua mensagem...'):
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    with st.chat_message('user'):
        st.markdown(prompt)

    with st.chat_message('assistant'):
        response = agent_executor.invoke({"input": prompt, "chat_history": []}).get('output')

        st.write(response)
        st.session_state.messages.append(
            {'role': 'assistant', 'content': response}
        )
