from fastapi import FastAPI

from src.main_routes import api_router
import src.constants as c

print(api_router)

app = FastAPI(
    title='A3Data CSV CHATBOT API',
    description='API for A3Data CSV Chatbot',
    openapi_url='/openapi.json',)
#
#
app.include_router(api_router, prefix=c.API_V1_STR)
