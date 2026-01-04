
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime, timezone

CURRENT_YEAR = datetime.now(timezone.utc).year

class BookBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    author: str = Field(..., min_length=1, max_length=255)
    genre: str = Field(..., min_length=1, max_length=100)
    year_published: int = Field(..., le=CURRENT_YEAR)
    summary: Optional[str] = Field(None, max_length=2000)

    @field_validator("title", "author", "genre", mode="before")
    @classmethod
    def strip_and_validate(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("Must not be empty or whitespace")
        return value

    @field_validator("year_published")
    @classmethod
    def validate_year(cls, value: int) -> int:
        if value > CURRENT_YEAR:
            raise ValueError("Publication year cannot be in the future")
        return value

class CreateBook(BookBase):
    pass

class GetBook(BookBase):
    id: int
    slug: str

    model_config = {"from_attributes": True}

class UpdateBook(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=255)
    author: Optional[str] = Field(None, min_length=1, max_length=255)
    genre: Optional[str] = Field(None, min_length=1, max_length=100)
    year_published: Optional[int] = Field(None, ge=1450, le=CURRENT_YEAR)
    summary: Optional[str] = Field(None, max_length=2000)

    @field_validator("title", "author", "genre", mode="before")
    @classmethod
    def strip_and_validate(cls, value: Optional[str]) -> Optional[str]:
        if value is None:
            return value
        value = value.strip()
        if not value:
            raise ValueError("Must not be empty or whitespace")
        return value

    @field_validator("year_published")
    @classmethod
    def validate_year(cls, value: Optional[int]) -> Optional[int]:
        if value is None:
            return value
        if value > CURRENT_YEAR:
            raise ValueError("Publication year cannot be in the future")
        return value
