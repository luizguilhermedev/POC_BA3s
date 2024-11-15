from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains.retrieval import create_retrieval_chain

from src.utils import get_llm_model, get_retriever
from src.prompts import instruction_prompt

llm = get_llm_model(use_openai=False)
retriever = get_retriever()

question_answer_chain = create_stuff_documents_chain(llm, instruction_prompt)
rag_chain = create_retrieval_chain(retriever, question_answer_chain)


answer = rag_chain.invoke(
    {'input': 'Quais autores mais venderam por categoria?'}
)
print(answer['answer'])
