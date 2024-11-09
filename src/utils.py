import os

from langchain_openai import ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


def get_llm_model():
    model_openai = ChatOpenAI(
        temperature=0.2,
        model="gpt-4o",
        openai_api_key=OPENAI_API_KEY)

    return model_openai
