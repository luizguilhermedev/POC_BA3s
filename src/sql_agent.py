import os

from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
from operator import itemgetter
from langchain_community.agent_toolkits import create_sql_agent
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


import streamlit as st

from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

db = SQLDatabase.from_uri("sqlite:///books.db")

model = ChatGroq(
    model='llama-3.1-70b-versatile',
    api_key=GROQ_API_KEY
)

agent = create_sql_agent(
    llm=llm,
    db=db,
    prompt=full_prompt,
    verbose=True,
    agent_type="openai-tools",
)
agent_executor = create_sql_agent(model, db=db, agent_type="openai-tools", verbose=True)
print(agent_executor.invoke({"input": "Quais são os livros mais populares?"}))


def initialize_chatbot_ui():
    """Function to initialize the chatbot UI using Streamlit"""
    st.title('BA3s - v0.2   ')

    session_id = st.sidebar.text_input('Your Session ID Here')
    config = {'configurable': {'session_id': session_id}}

    if 'messages' not in st.session_state:
        st.session_state.messages = []

    st.chat_message('ai').write(
        'Olá, sou BA3s, especialista em análise de avaliações de livros. Como posso ajudar você hoje?'
    )

    for message in st.session_state.messages:
        with st.chat_message(message['role']):
            st.write(message['content'])

    if prompt := st.chat_input('Sua mensagem...'):
        st.session_state.messages.append({'role': 'user', 'content': prompt})

        with st.chat_message('user'):
            st.markdown(prompt)

        with st.chat_message('assistant'):
            response = ask_your_data(prompt, config)
            executable_code = extract_code_from_response(response)

            if executable_code:

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
                        'Enviroment': PythonREPL,
                    },
                )
                sys.stdout = old_stdout
                output = new_stdout.getvalue()

                fig = plt.gcf()

                if fig.get_axes():
                    st.pyplot(fig)
                else:
                    st.write(response)
                    st.write(output)
            else:
                st.write(response)
                st.session_state.messages.append(
                    {'role': 'assistant', 'content': response}
                )
