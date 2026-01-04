from fastapi import FastAPI
from api.routes import api_router
from core.config import settings

app = FastAPI(
    title=settings.PROJECT_TITLE,
    version=settings.PROJECT_VERSION
)

app.include_router(api_router)


@app.get("/")
async def root():
    return {"message": "API is running"}