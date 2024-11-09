import os
import re
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

# from src.utils import get_agent, get_agent_with_prompt

from src.utils import get_agent_with_prompt


agent = get_agent_with_prompt(
    path=[
        'src/data/books_data_cleaned.csv',
        'src/data/books_rating_cleaned.csv',
    ]
)


def ask_your_data(input: str):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    response = agent.stream({'input': input})
    for chunk in response:
        response = chunk.get('output')
    return response


print()


def extract_code_from_response(response):
    """Extracts Python code from a string response."""
    # Use a regex pattern to match content between triple backticks
    code_pattern = r'```python(.*?)```'
    match = re.search(code_pattern, response, re.DOTALL)

    if match:
        # Extract the matched code and strip any leading/trailing whitespaces
        python_code = match.group(1).strip()
        modified_code = re.sub(
            r'dados\s*=\s*\{.*?}',
            'df = df',
            python_code,
            flags=re.DOTALL,
        )
        return modified_code

    return None


st.title('BA3s - v0.1')

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
    # Add user message to chat history
    st.session_state.messages.append({'role': 'user', 'content': prompt})
    # Display user message in chat message container
    with st.chat_message('user'):
        st.markdown(prompt)

    # Display assistant response in chat message container

    with st.chat_message('assistant'):
        response = ask_your_data(prompt)
        executable_code = extract_code_from_response(response)
        if executable_code:
            st.code(executable_code, language='python')
            exec(executable_code, globals(), {'df': pd.DataFrame(), 'plt': plt})
            fig = plt.gcf()  # Get current figure
            st.pyplot(fig)

        else:
            st.write(response)
    # with st.chat_message('assistant'):
    #     response = ask_your_data(prompt)
    #     st.spinner()
    #     st.write(response)
