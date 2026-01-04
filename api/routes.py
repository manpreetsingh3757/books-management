from fastapi import APIRouter
from core.config import settings 
from api.v1.users_route import router as user_router
from api.v1.auth_route import router as auth_router
from api.v1.books_route import router as books_router
from api.v1.reviews_route import router as reviews_router
from api.v1.ai_routes import router as ai_router


api_router = APIRouter(
    prefix=f"/api/{settings.API_VERSION}"
)

api_router.include_router(user_router)
api_router.include_router(auth_router)
api_router.include_router(books_router)
api_router.include_router(reviews_router)
api_router.include_router(ai_router)
