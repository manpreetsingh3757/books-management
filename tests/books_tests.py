import pytest
import pytest_asyncio
from core.database import AsyncSessionLocal
from core.database import Base
from users.models import User
from reviews.models import Review
from books.models import Book
from books.services import BookService
from books.schemas import CreateBook

__all__ = ["Base", "User", "Review", "Book"]

@pytest_asyncio.fixture
async def db_session():
    """
    Provide an async database session for tests.
    """
    async with AsyncSessionLocal() as session:
        yield session

@pytest.mark.asyncio
async def test_create_and_get_book_success(db_session):
    service = BookService(db_session)

    book = await service.create_book(
        CreateBook(title = "And Then There Were None", author= "Agatha Christie", genre= "Mystery", year_published= 1939, summary= "Ten strangers invited to a remote island uncover a deadly secret")
    )

    fetched = await service.get_book(book.slug)

    assert fetched.slug == book.slug