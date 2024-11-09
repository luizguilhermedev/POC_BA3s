import logging

from fastapi import APIRouter

import src.utils
from src.utils import MessagePayload
agent = src.utils.get_agent(path=['data/books_data_cleaned.csv',
                                  'data/books_rating_cleaned.csv', ])
router = APIRouter()


@router.post('/', response_model=MessagePayload)
def ask_your_data(payload: MessagePayload):
    """Function to handle the MessagePayload and return the response from the Agent model"""

    response = agent.stream(payload.input)
    answer = ''
    for chunk in response:
        answer += chunk
    logging.debug(f'Answer: {answer}')

    return answer

