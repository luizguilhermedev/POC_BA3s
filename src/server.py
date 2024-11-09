from fastapi import FastAPI

from src.main_routes import api_router
import constants as c

print(api_router)

app = FastAPI(
    title='A3Data CSV CHATBOT API',
    description='API for A3Data CSV Chatbot',
    openapi_url='/openapi.json',)
#
#
app.include_router(api_router, prefix=c.API_V1_STR)



if __name__ == '__main__':
    import uvicorn

    uvicorn.run(
        'src.server:app',
        host=c.APP_HOST,
        port=c.APP_PORT,
        log_level=c.LOG_LEVEL,
        reload=True,
    )

