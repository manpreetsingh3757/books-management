import pytest
import pytest_asyncio
from uuid import uuid4
from core.database import Base
from core.database import AsyncSessionLocal, engine
from auth.services import AuthService
from auth import  schemas as auth_schemas
from auth import constants
from users.models import User
from users.services import UserService
from users import schemas
from reviews.models import Review
from books.models import Book

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
async def test_create_and_get_user_success(db_session):
    service = UserService(db_session)

    user = await service.register_user(
        schemas.CreateUser(email="marcowillt@test.com", password="passwordtest")
    )

    fetched = await service.get_user(user.id)

    assert fetched.id == user.id
    assert fetched.email == user.email


@pytest.mark.asyncio
async def test_create_user_duplicate_email(db_session):
    service = UserService(db_session)

    payload = schemas.CreateUser(email="dupemail1@test.com", password="password123")
    await service.register_user(payload)

    with pytest.raises(Exception) as exc_info:
        await service.register_user(payload)

    assert "already exists" in str(exc_info.value)


@pytest.mark.asyncio
async def test_get_user_success(db_session):
    service = UserService(db_session)
    payload = schemas.CreateUser(email="getuser1@test.com", password="password123")
    user = await service.register_user(payload)

    fetched = await service.get_user(user.id)

    assert fetched.id == user.id
    assert fetched.email == user.email


@pytest.mark.asyncio
async def test_get_user_not_found(db_session):
    service = UserService(db_session)
    fake_id = uuid4()

    with pytest.raises(Exception) as exc_info:
        await service.get_user(fake_id)

    assert "not found" in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_user_success(db_session):
    # Create user first
    user_service = UserService(db_session)
    payload = schemas.CreateUser(email="loginuser1@test.com", password="mypassword")
    user = await user_service.register_user(payload)

    auth_service = AuthService(db_session)
    login_payload = auth_schemas.LoginUser(email="loginuser1@test.com", password="mypassword")
    token = await auth_service.login_user(login_payload)

    assert token.access_token is not None
    assert token.token_type == "bearer"


@pytest.mark.asyncio
async def test_login_user_invalid_email(db_session):
    auth_service = AuthService(db_session)
    login_payload = auth_schemas.LoginUser(email="invalid1@test.com", password="somepass")

    with pytest.raises(Exception) as exc_info:
        await auth_service.login_user(login_payload)

    assert constants.INVALID_EMAIL in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_user_invalid_password(db_session):
    # Create user
    user_service = UserService(db_session)
    payload = schemas.CreateUser(email="wrongpass1@test.com", password="correctpass")
    await user_service.register_user(payload)

    auth_service = AuthService(db_session)
    login_payload = auth_schemas.LoginUser(email="wrongpass1@test.com", password="wrongpass")

    with pytest.raises(Exception) as exc_info:
        await auth_service.login_user(login_payload)

    assert constants.INVALID_PASSWORD in str(exc_info.value)


@pytest.mark.asyncio
async def test_login_user_inactive_user(db_session):
    # Create user
    user_service = UserService(db_session)
    payload = schemas.CreateUser(email="inactive1@test.com", password="pass12345678")
    user = await user_service.register_user(payload)

    # Manually set user inactive
    user.is_active = False
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    auth_service = AuthService(db_session)
    login_payload = auth_schemas.LoginUser(email="inactive1@test.com", password="pass12345678")

    with pytest.raises(Exception) as exc_info:
        await auth_service.login_user(login_payload)

    assert constants.USER_INACTIVE in str(exc_info.value)