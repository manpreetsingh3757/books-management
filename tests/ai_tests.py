import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from core.database import AsyncSessionLocal, engine
from users.models import User
from users.services import UserService
from users import schemas as user_schemas
from books.models import Book
from books.services import BookService
from books import schemas as book_schemas
from ai_features.services import AIService, RecommendedAIService, GenerateSummaryAIService
from ai_features.schemas import SummaryResponse


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
async def test_book_summary_success(db_session):

    user_service = UserService(db_session)
    user = await user_service.register_user(user_schemas.CreateUser(email="aiuser@test.com", password="password12345678"))

    book_service = BookService(db_session)
    book = await book_service.create_book(
        book_schemas.CreateBook(
            title="AI Book",
            author="Author AI",
            genre="Fiction",
            year_published=2023
        )
    )

    service = AIService(db_session)

    with patch.object(service.helper, 'get_book', new=AsyncMock(return_value=book)), \
         patch.object(service.helper, 'get_reviews', new=AsyncMock(return_value=([], 0, 0))), \
         patch('ai_features.services.client_call', return_value="AI summary"):

        response = await service.book_summary(book.slug)
        assert isinstance(response, SummaryResponse)
        assert response.summary == "AI summary"


@pytest.mark.asyncio
async def test_books_recommendation_success(db_session):
    user_service = UserService(db_session)
    user = await user_service.register_user(user_schemas.CreateUser(email="recommender@test.com", password="password123"))

    service = RecommendedAIService(db_session, user)

    with patch.object(service.helper, 'get_user_liked_books', new=AsyncMock(return_value=[])), \
         patch.object(service.helper, 'get_top_rated_books', new=AsyncMock(return_value=[])), \
         patch('ai_features.services.client_call', return_value="Recommended books"), \
         patch.object(service.prompt_helper, 'get_prompt_message', return_value="mock message"):

        response = await service.books_recommedation()
        assert isinstance(response, SummaryResponse)
        assert response.summary == "Recommended books"


@pytest.mark.asyncio
async def test_generate_summary_success(db_session):
    service = GenerateSummaryAIService(db_session)
    content = "Some content to summarize"

    with patch.object(service.prompt_helper, 'get_prompt_message', return_value="mock message"), \
         patch('ai_features.services.client_call', return_value="Generated summary"):

        response = await service.generate_summary(content)
        assert isinstance(response, SummaryResponse)
        assert response.summary == "Generated summary"
