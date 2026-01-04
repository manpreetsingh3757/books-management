import pytest
import pytest_asyncio
from core.database import AsyncSessionLocal, engine
from core.database import Base
from users.models import User
from reviews.models import Review
from books.models import Book
from books.services import BookService
from books import schemas
from books import constants

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
async def test_create_book_success(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="Test Book",
        author="Author One",
        genre="Fiction",
        year_published=2023,
        summary="A test book"
    )
    book = await service.create_book(payload)

    assert book.id is not None
    assert book.title == "Test Book"
    assert book.slug is not None


@pytest.mark.asyncio
async def test_create_book_duplicate_title_author(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="Unique Book",
        author="Author Dup",
        genre="Fiction",
        year_published=2023,
        summary="Duplicate test"
    )
    await service.create_book(payload)

    with pytest.raises(Exception) as exc_info:
        await service.create_book(payload)
    assert "already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_all_books(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="All Books Test",
        author="Author AB",
        genre="Fiction",
        year_published=2022
    )
    await service.create_book(payload)

    books = await service.get_all_books()
    assert isinstance(books, list)
    assert len(books) > 0


@pytest.mark.asyncio
async def test_get_book_success(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="Fetch Book",
        author="Author FB",
        genre="Fiction",
        year_published=2021
    )
    book = await service.create_book(payload)

    fetched = await service.get_book(book.slug)
    assert fetched.id == book.id
    assert fetched.title == "Fetch Book"


@pytest.mark.asyncio
async def test_get_book_not_found(db_session):
    service = BookService(db_session)
    fake_slug = "non-existent-slug"

    with pytest.raises(Exception) as exc_info:
        await service.get_book(fake_slug)

    assert constants.BOOK_NOT_FOUND in str(exc_info.value)


@pytest.mark.asyncio
async def test_update_book_success(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="Book To Update",
        author="Author Update",
        genre="Fiction",
        year_published=2020
    )
    book = await service.create_book(payload)

    update_payload = schemas.UpdateBook(title="Updated Book Title")
    updated = await service.update_book(book.slug, update_payload)

    assert updated.title == "Updated Book Title"


@pytest.mark.asyncio
async def test_update_book_not_found(db_session):
    service = BookService(db_session)
    fake_slug = "update-fake-slug"
    update_payload = schemas.UpdateBook(title="Won't work")

    with pytest.raises(Exception) as exc_info:
        await service.update_book(fake_slug, update_payload)

    assert constants.BOOK_NOT_FOUND in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_book_success(db_session):
    service = BookService(db_session)
    payload = schemas.CreateBook(
        title="Book To Delete",
        author="Author Delete",
        genre="Fiction",
        year_published=2019
    )
    book = await service.create_book(payload)

    result = await service.delete_book(book.slug)
    assert result["message"] == constants.BOOK_DELETED

    with pytest.raises(Exception) as exc_info:
        await service.get_book(book.slug)
    assert constants.BOOK_NOT_FOUND in str(exc_info.value)


@pytest.mark.asyncio
async def test_delete_book_not_found(db_session):
    service = BookService(db_session)
    fake_slug = "delete-fake-slug"

    with pytest.raises(Exception) as exc_info:
        await service.delete_book(fake_slug)
    assert constants.BOOK_NOT_FOUND in str(exc_info.value)