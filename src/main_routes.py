from fastapi import APIRouter

from src import chat_route

api_router = APIRouter()

api_router.include_router(chat_route.router, prefix='/chat')

