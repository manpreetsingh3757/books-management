import pytest
import pytest_asyncio
from core.database import Base
from core.database import AsyncSessionLocal
from users.models import User
from users.services import UserService
from users.schemas import CreateUser
from reviews.models import Review
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
async def test_create_and_get_user_success(db_session):
    service = UserService(db_session)

    user = await service.register_user(
        CreateUser(email="johnwill@test.com", password="passwordtest")
    )

    fetched = await service.get_user(user.id)

    assert fetched.id == user.id
    assert fetched.email == user.email