import logging

from fastapi import APIRouter, HTTPException

from src.chat import a3_data_agent
from api.api_utils import MessagePayload

router = APIRouter()


@router.post('/ask_your_data', response_model=MessagePayload)
def ask_your_data(payload: MessagePayload):
    """Function to handle the MessagePayload and return the response from the Agent model"""

    response = a3_data_agent.stream(payload.input)
    answer = ''
    async for chunk in response:
        answer += chunk
    logging.debug(f'Answer: {answer}')

    return answer

