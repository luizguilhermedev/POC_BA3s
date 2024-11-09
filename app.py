import os
import re
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

from src.utils import get_agent

agent = get_agent(path=['src/data/books_data_cleaned.csv', 'src/data/books_rating_cleaned.csv'])

def ask_your_data(input: str):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    response = agent.stream({'input': input})
    for chunk in response:
        response = chunk.get('output')

    return response


def extract_code_from_response(response):
    """Extracts Python code from a string response."""
    # Use a regex pattern to match content between triple backticks
    code_pattern = r"```python(.*?)```"
    match = re.search(code_pattern, response, re.DOTALL)

    if match:
        # Extract the matched code and strip any leading/trailing whitespaces
        print("code here")
        return match.group(1).strip()

    return None


st.title('BA3s - v0.1')


if 'messages' not in st.session_state:
    st.session_state.messages = []
st.chat_message('ai').write('Olá, sou BA3s, especialista em análise de avaliações de livros. Como posso ajudar você hoje?')

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
        st.spinner()
        st.write(response)


        # executable_code = extract_code_from_response(response)
        # if executable_code:
        #     print(executable_code)
        #     st.code(executable_code)
        #     exec(executable_code, globals(), {'st': st, 'pd': pd, 'plt': plt})
        #     fig = plt.gcf()  # Get current figure
        #     st.pyplot(fig)  # Display using Streamlit


