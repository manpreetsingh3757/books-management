import uuid
from pydantic import BaseModel, Field

class ReviewCreate(BaseModel):
    review_text: str = Field(..., min_length=10)
    rating: int = Field(..., ge=1, le=5)

class ReviewResponse(BaseModel):
    id: int
    user_id: uuid.UUID
    review_text: str
    rating: int

    class Config:
        from_attributes = True
