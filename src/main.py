from fastapi import FastAPI

from src.views import router

app: FastAPI = FastAPI()
app.include_router(router)
