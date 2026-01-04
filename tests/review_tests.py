import pytest
import pytest_asyncio
from sqlalchemy import select
from core.database import Base
from core.database import AsyncSessionLocal
from users.models import User
from reviews.models import Review
from reviews.services import ReviewService
from reviews.schemas import ReviewCreate
from books.models import Book

__all__ = ["Base", "User", "Review", "Book"]

@pytest_asyncio.fixture
async def db_session():
    """
    Provide an async database session for tests.
    """
    async with AsyncSessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_create_book_review(db_session):
    service = ReviewService(db_session)

    user_query = await db_session.execute(
        select(User).order_by(User.id.desc()).limit(1)
    )
    last_user = user_query.scalar_one_or_none()

    book_query = await db_session.execute(
        select(Book).order_by(Book.id.desc()).limit(1)
    )
    last_book = book_query.scalar_one_or_none()
    
    await service.add_review(last_book.slug, last_user, 
        ReviewCreate(review_text="Excelent book, recommended", rating=4)
    )