import io
import sys
import src.constants as c
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils import conversational_chain, extract_code_from_response
from langchain_experimental.utilities import PythonREPL

import streamlit as st

chain = conversational_chain(c.PATH_TO_FILE)

# TODO: Add instruction to prompts
instruction = """You are a expert in data analysis.
You can have conversations normally with the user.
You have full access to df1 and df2. Use full dataset not only the head().
You can answer questions, generate code, charts or graphs. Only generate code if you are asked to or if you are asked to generate charts or graphs.
If you need to code, use python language.
Only generates code if you are asked to or if you are asked to generate charts or graphs
If you need to run code, runtime: PythonREPL if your answer is not a code, give it as a text"""


def ask_your_data(input: str, config: dict = None):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    input = input + instruction
    response = chain.stream({'input': input}, config=config)

    #
    # return response
    # response = get_agent(c.PATH_TO_FILE).run(input)
    #
    # return response

    for chunk in response:
        model_answer = chunk.get('output')
    return model_answer


def initialize_chatbot_ui():
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
            # st.markdown(message['content'])
            st.write(message['content'])
    # Accept user input
    if prompt := st.chat_input('Sua mensagem...'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            response = ask_your_data(prompt, config)
            executable_code = extract_code_from_response(response)

            if executable_code:
                print('entrou aqui')  # TODO: Arrumar como o codio esta vindo aqui
                try:
                    print(executable_code)
                    old_stdout = sys.stdout
                    new_stdout = io.StringIO()
                    sys.stdout = new_stdout

                    st.code(executable_code, language='python')
                    exec(
                        executable_code,
                        globals(),
                        {
                            'df': pd.DataFrame(),
                            'df1': pd.read_csv('src/data/books_data_sample.csv'),
                            'df2': pd.read_csv('src/data/books_rating_sample.csv'),
                            'plt': plt,
                            'sns': sns,
                            'PythonREPL': PythonREPL,
                            'environment': PythonREPL,
                            'language': 'python',
                        },
                    )

                    sys.stdout = old_stdout

                    output = new_stdout.getvalue()
                    st.write(output)

                    fig = plt.gcf()
                    st.pyplot(fig)
                except:
                    st.write(response)
                    st.session_state.messages.append(
                        {'role': 'assistant', 'content': response}
                    )
            else:
                st.write(response)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response}
                )
