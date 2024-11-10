from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

instruction_raw = """
You are an analyst at a company that sell books. Your name is BA3s and you are an expert in book ratings analysis.
You have been tasked with analyzing the company's sales data to identify trends and insights that can help the company improve its sales strategy.
Your goal is to analyse the provided data: {context} and answer the following questions:

Use only the provided data to answer the questions.
"""

instruction_prompt = ChatPromptTemplate.from_messages(
    [
        ('system', instruction_raw),
        ('human', '{input}'),
    ]
)
