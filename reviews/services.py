
from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from books import constants
from books.models import Book
from reviews import schemas
from reviews.models import Review
from reviews.helper import ReviewHelper

class ReviewService:
    """
    Review based services
    """
    
    def __init__(self, db: AsyncSession):
        self.db = db
        self.helper = ReviewHelper(self.db)

    async def add_review(self, book_slug: str, auth_user: User, payload: schemas.ReviewCreate) -> Review:
        """
        Add reviews and ratings for selected book
        """

        result = await self.db.execute(select(Book).where(Book.slug == book_slug))
        book = result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.BOOK_NOT_FOUND)

        return await self.helper.create(
            book_id=book.id,
            user=auth_user,
            review_text=payload.review_text,
            rating=payload.rating,
        )
    
    async def get_all_reviews(self, book_slug: str) -> List[Review]:
        """
        Fetch all ratings and reviews based on selected book
        """

        book_result = await self.db.execute(select(Book).where(Book.slug == book_slug))
        book = book_result.scalar_one_or_none()
        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.BOOK_NOT_FOUND)
        
        return await self.helper.list_by_book(book.id)