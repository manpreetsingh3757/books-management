from fastapi import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.dependencies import verify_token
from reviews import schemas, services


router = APIRouter(prefix="/books")

@router.post("/{book_slug}/reviews/", response_model=schemas.ReviewResponse, status_code=status.HTTP_201_CREATED)
async def add_review(book_slug: str, payload: schemas.ReviewCreate, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.ReviewService(db)
    return await service.add_review(book_slug, auth_user, payload)

@router.get("/{book_slug}/reviews/", response_model=list[schemas.ReviewResponse])
async def get_reviews(book_slug: str, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.ReviewService(db)
    return await service.get_all_reviews(book_slug)