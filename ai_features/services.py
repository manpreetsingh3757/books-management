
from core.config import settings
from huggingface_hub import InferenceClient
from sqlalchemy.ext.asyncio import AsyncSession
from users.models import User
from ai_features.prompt_helper.books_summary import PromptHelper
from ai_features.prompt_helper.books_recommendation import RecommendedPromptHelper
from ai_features.prompt_helper.generate_summary import GenerateSummaryPromptHelper
from ai_features.helper import BookSummaryHelper, RecommendationHelper
from ai_features.schemas import SummaryResponse



def client_call(message):
    """
    A function which used to connect with model and generate a AI response.
    """

    try:
        client = InferenceClient(api_key=settings.ai_model_key)
        model = settings.ai_model
        response = client.chat.completions.create(
                    model=model,
                    messages=message,
                )
        return response.choices[0].message["content"]
    except Exception:
        return "Somethin went wrong."

class AIService:
    """
    Class base service for book summary.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.prompt_helper = PromptHelper()
        self.helper = BookSummaryHelper(self.db)

    async def book_summary(self, book_slug: str) -> str:
        """
        Generates a summary of a book according to available title and reviews.
        """
        book_obj = await self.helper.get_book(book_slug)
        reviews, average_rating, total_reviews = await self.helper.get_reviews(book_obj.id)
        message = self.prompt_helper.get_prompt_message(book_obj, reviews, average_rating, total_reviews)
        
        return SummaryResponse(
            summary= client_call(message)
        )

class RecommendedAIService:
    """
    Class base service for book recommendation.
    """
    def __init__(self, db: AsyncSession, auth_user: User):
        self.db = db
        self.auth_user = auth_user
        self.prompt_helper = RecommendedPromptHelper()
        self.helper = RecommendationHelper(self.db)

    async def books_recommedation(self) -> str:
        """
        Recommended top rated books stored in DB, acc. to user perfernce.
        User perfernce decide on review added by user.
        """
        liked_books = await self.helper.get_user_liked_books(self.auth_user.id)
        top_rated_books = await self.helper.get_top_rated_books(self.auth_user.id)
        message = self.prompt_helper.get_prompt_message(liked_books, top_rated_books)
        
        return SummaryResponse(
            summary= client_call(message)
        )

class GenerateSummaryAIService:
    """
    Class base service for book genrate book summary.
    """

    def __init__(self, db: AsyncSession):
        self.db = db
        self.prompt_helper = GenerateSummaryPromptHelper()

    async def generate_summary(self, content:str) -> str:
        """
        Generates a summary of a book on base of provided content.
        """
        message = self.prompt_helper.get_prompt_message(content)
        
        return SummaryResponse(
            summary= client_call(message)
        )