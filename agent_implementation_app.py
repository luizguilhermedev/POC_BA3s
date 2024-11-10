import os
import re
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from langchain_core.runnables import RunnableWithMessageHistory

import src.constants as c
from src.utils import get_agent, create_session_factory, InputChat

agent = get_agent(c.PATH_TO_FILE)

chain_with_history = RunnableWithMessageHistory(
    agent,
    create_session_factory("chat_histories")
).with_types(input_type=InputChat)


def ask_your_data(input: str, config: dict = None):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    response = chain_with_history.stream({'input': input}, config=config)

    for chunk in response:
        answer = chunk.get('output')
    return answer


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
        response = ask_your_data(prompt, config)
        st.spinner('Analisando...')
        executable_code = extract_code_from_response(response)
        if executable_code:

            st.code(executable_code, language='python')
            exec(
                executable_code, globals(), {'df': pd.DataFrame(), 'plt': plt}
            )
            fig = plt.gcf()  # Get current figure
            st.pyplot(fig)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': response}
            )

        else:
            st.spinner('Analisando...')

            st.write(response)
            st.session_state.messages.append(
                {'role': 'assistant', 'content': response}
            )
