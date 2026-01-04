from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.dependencies import verify_token
from ai_features.services import AIService, RecommendedAIService, GenerateSummaryAIService
from ai_features.schemas import SummaryResponse, ContentResponse


router = APIRouter()

@router.get("/books/{book_slug}/summary", response_model=SummaryResponse)
async def generate_summary(book_slug: str, auth_user: None = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    service = AIService(db)
    return await service.book_summary(book_slug)

@router.get("/recommendations", response_model=SummaryResponse)
async def generate_summary(auth_user: None = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    service = RecommendedAIService(db, auth_user)
    return await service.books_recommedation()

@router.get("/generate-summary", response_model=SummaryResponse)
async def generate_summary(payload: ContentResponse, auth_user: None = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    service = GenerateSummaryAIService(db)
    return await service.generate_summary(payload)