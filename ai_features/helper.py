from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from books.models import Book
from books import constants
from reviews.helper import ReviewHelper
from reviews.models import Review
from ai_features.schemas import UserPreferenceBook, RecommendedBooks


class BookSummaryHelper:
    """
    Helper class for book summary DB operations
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_book(self, slug: str):
        """
        Fetch book object from DB
        """
        
        stmt = select(Book).where(Book.slug == slug)
        result = await self.db.execute(stmt)
        book =  result.scalar_one_or_none()
        if not book:
            raise HTTPException(
                            status_code=status.HTTP_409_CONFLICT,
                            detail=constants.BOOK_NOT_FOUND
                        )
        return book

    async def get_reviews(self, book_id: int):
        """
        Fetch all reviews which is realted to selected book
        """
        
        helper = ReviewHelper(self.db)

        reviews = await helper.list_by_book(book_id)

        total_ratings = [r.rating for r in reviews if r.rating is not None]
        total_reviews = len(total_ratings)
        formatted_reviews = "\n".join(
                    f"- {r.review_text} (Rating: {r.rating})"
                    for r in reviews[:10]
                )
        
        if total_reviews == 0:
            return "", 0.0, 0

        average_rating = sum(total_ratings) / total_reviews
        return formatted_reviews, round(average_rating, 2), total_reviews


class RecommendationHelper:
    """
    Helper class for book recommendation DB operations
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_liked_books(self, user_id: UUID) -> list[dict]:
        """
        Fetch books reviewed by the user with rating >= 4
        and return books and ratings JSON data.
        """

        stmt = (
            select(
                Book.title,
                Book.genre,
                Book.summary,
                Review.review_text,
                
            )
            .join(Book, Book.id == Review.book_id)
            .where(
                Review.user_id == user_id,
                Review.rating >= 4
            )
            .order_by(Review.rating.desc())
            .limit(10)
        )


        result = await self.db.execute(stmt)
        rows = result.all()

        return [UserPreferenceBook.model_validate(row) for row in rows]

    async def get_top_rated_books(self, user_id: UUID) -> list[dict]:
        """
        Fetch top-rated books excluding those already reviewed by the user.
        """

        reviewed_books_subq = (
            select(Review.book_id)
            .where(Review.user_id == user_id)
            .subquery()
        )

        stmt = (
            select(
                Book.title,
                Book.genre,
                Book.summary,
                func.avg(Review.rating).label("avg_rating")
            )
            .join(Review, Review.book_id == Book.id)
            .where(Book.id.not_in(reviewed_books_subq))
            .group_by(Book.id)
            .order_by(func.avg(Review.rating).desc())
            .limit(10)
        )

        result = await self.db.execute(stmt)
        rows = result.all()

        return [RecommendedBooks.model_validate(row) for row in rows]
