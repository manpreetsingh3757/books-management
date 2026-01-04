from pydantic import BaseModel
from typing import Optional

class UserPreferenceBook(BaseModel):
    title: str
    genre: str
    summary: Optional[str]
    review_text: Optional[str]

    class Config:
        from_attributes = True

class RecommendedBooks(BaseModel):
    title: str
    genre: str
    summary: Optional[str]
    rating: float

    class Config:
        from_attributes = True

class ContentResponse(BaseModel):
    content: str

class SummaryResponse(BaseModel):
    summary: str

    class Config:
        from_attributes = True