from fastapi import APIRouter

from src.chat_route import chat

api_router = APIRouter()

api_router.include_router(chat.router, prefix='/chat')

