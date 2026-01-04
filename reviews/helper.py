from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from reviews.models import Review
from users.models import User

class ReviewHelper:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, *, book_id: int, user: User, review_text: str, rating: int) -> Review:
        
        review = Review(
            book_id=book_id,
            user_id=user.id,
            review_text=review_text,
            rating=rating
        )
        self.db.add(review)
        await self.db.commit()
        await self.db.refresh(review)
        return review

    async def list_by_book(self, book_id: int) -> list[Review]:

        stmt = select(Review).where(Review.book_id == book_id)
        result = await self.db.execute(stmt)
        return result.scalars().all()