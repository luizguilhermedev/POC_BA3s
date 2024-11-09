import logging

from fastapi import APIRouter

from langchain_core.prompts import ChatPromptTemplate
import src.utils
from src.utils import MessagePayload

agent = src.utils.get_agent(path=['data/books_data_cleaned.csv',
                                  'data/books_rating_cleaned.csv', ])
router = APIRouter()



prompt = ChatPromptTemplate.from_messages(
    [
        ('system', 'You are a helpull assistant that can help me with my book search.'),
        ('human', '{input}'),
    ]
)
@router.post('/', response_model=MessagePayload)
async def ask_your_data(payload: MessagePayload):
    """Function to handle the MessagePayload and return the response from the Agent model"""
    response = agent.stream({'input': payload.input})
    for chunk in response:
        response = chunk.get('output')

    req_response = MessagePayload.model_validate(
        {'input': payload.input, 'output': response}
    )

    return req_response
