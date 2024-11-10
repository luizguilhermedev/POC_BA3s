import os

from langchain_community.document_loaders import DirectoryLoader
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import CharacterTextSplitter

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_groq import ChatGroq
from langchain.agents.agent_types import AgentType
from langchain_experimental.agents.agent_toolkits import create_csv_agent
from langchain_experimental.text_splitter import SemanticChunker

from pydantic import BaseModel

from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

GROQ_API_KEY = os.getenv('GROQ_API_KEY')

load_dotenv()


def get_llm_model(use_openai: bool = True):
    if use_openai:
        model_openai = ChatOpenAI(
            temperature=0.2, model='gpt-4o', openai_api_key=OPENAI_API_KEY
        )

        return model_openai

    model = ChatGroq(
        model="llama-3.1-70b-versatile",
        temperature=0,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )
    return model


def get_agent(path: list[str]):
    return create_csv_agent(
        get_llm_model(),
        path=path,
        agent_type=AgentType.OPENAI_FUNCTIONS,
        verbose=True,
        allow_dangerous_code=True,
        handle_parsing_errors=True,
    )


def get_embedding_model():
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-mpnet-base-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': False}
    )
    return embeddings


# def get_spliiter():
#     splitter = CharacterTextSplitter
#     return splitter

def ingest_data(path):
    # Load the data

    loader = DirectoryLoader(path, glob='**/*.csv', loader_cls=CSVLoader)
    documents = loader.load_and_split()

    # docs = get_spliiter().split_documents(documents)

    vector_db = Chroma.from_documents(documents, embedding=get_embedding_model(), persist_directory='vectordb_data/')

    if not vector_db:
        return None

    return "Ingested data successfully"


def get_retriever():
    vector_store = Chroma(
        embedding_function=get_embedding_model(),
        persist_directory="vectordb/",
    )

    return vector_store.as_retriever()


ingest = ingest_data("data/")


# Pydantic models to be used with FastAAPI
class MessagePayload(BaseModel):
    """MessagePayload class to handle the input from the user"""

    input: str
    output: str
