import pytest
import pytest_asyncio
from sqlalchemy import select
from core.database import Base
from core.database import AsyncSessionLocal, engine
from users.models import User
from users.services import UserService
from users import schemas as user_schemas
from reviews.models import Review
from reviews.services import ReviewService
from reviews import schemas
from books import constants
from books.models import Book
from books.services import BookService
from books import schemas as book_schemas

__all__ = ["Base", "User", "Review", "Book"]


@pytest_asyncio.fixture
async def db_session():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.rollback()
            await session.close()
            await engine.dispose()

@pytest.mark.asyncio
async def test_add_review_success(db_session):

    user_service = UserService(db_session)
    user = await user_service.register_user(
        user_schemas.CreateUser(email="reviewer2@test.com", password="password123")
    )

    # Create a book
    book_service = BookService(db_session)
    book = await book_service.create_book(
        book_schemas.CreateBook(
            title="Reviewable Bookn2",
            author="Author R",
            genre="Fiction",
            year_published=2023
        )
    )

    # Add review
    review_service = ReviewService(db_session)
    payload = schemas.ReviewCreate(review_text="Great book!", rating=5)
    review = await review_service.add_review(book.slug, user, payload)

    assert review.id is not None
    assert review.review_text == "Great book!"
    assert review.rating == 5
    assert review.book_id == book.id
    assert review.user_id == user.id


@pytest.mark.asyncio
async def test_add_review_book_not_found(db_session):
    user_service = UserService(db_session)
    user = await user_service.register_user(
        user_schemas.CreateUser(email="nobook2@test.com", password="password123")
    )

    review_service = ReviewService(db_session)
    payload = schemas.ReviewCreate(review_text="amazing book, evrybody must read it", rating=4)

    with pytest.raises(Exception) as exc_info:
        await review_service.add_review("non-existent-slug", user, payload)

    assert constants.BOOK_NOT_FOUND in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_all_reviews_success(db_session):
    # Create user and book
    user_service = UserService(db_session)
    user = await user_service.register_user(
        user_schemas.CreateUser(email="allreviews2@test.com", password="password123")
    )
    book_service = BookService(db_session)
    book = await book_service.create_book(
        book_schemas.CreateBook(
            title="Book With ReviewsN2",
            author="Author AR",
            genre="Fiction",
            year_published=2022
        )
    )

    # Add two reviews
    review_service = ReviewService(db_session)
    await review_service.add_review(book.slug, user, schemas.ReviewCreate(review_text="First review for book", rating=5))
    await review_service.add_review(book.slug, user, schemas.ReviewCreate(review_text="Second review for book", rating=4))

    reviews = await review_service.get_all_reviews(book.slug)
    assert len(reviews) == 2
    assert reviews[0].book_id == book.id
    assert reviews[1].book_id == book.id


@pytest.mark.asyncio
async def test_get_all_reviews_book_not_found(db_session):
    review_service = ReviewService(db_session)

    with pytest.raises(Exception) as exc_info:
        await review_service.get_all_reviews("non-existent-slug")

    assert constants.BOOK_NOT_FOUND in str(exc_info.value)
