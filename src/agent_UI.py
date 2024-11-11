import src.constants as c
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from src.utils import conversational_chain, extract_code_from_response

import streamlit as st

chain = conversational_chain(c.PATH_TO_FILE)

instruction = """You are a expert in data analysis. You can have conversations normally with the user.
 You have full access to df1 and df2. do not inform codes in your answer.não imprima dataframes nas respostas."""
def ask_your_data(input: str, config: dict = None):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    input = input + instruction
    response = chain.stream({'input': input}, config=config)

    # return response
    # response = get_agent(c.PATH_TO_FILE).run(input)

    # return response
    #
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

        # with st.chat_message('user'):
        #     st.markdown(prompt)

        with st.chat_message('assistant'):
            response = ask_your_data(prompt, config)
            executable_code = extract_code_from_response(response)

            if executable_code:
                try:
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
                        },
                    )
                    fig = plt.gcf()  # Get current figure
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
"""correlação entre nota media e frequencia de recomendação"""