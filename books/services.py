from fastapi import HTTPException, status
from typing import List
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from books import constants
from books.models import Book
from books.schemas import CreateBook, UpdateBook
from books.helper import generate_unique_slug, get_by_title_author

class BookService:
    """
    Book related services.
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_book(self, payload: CreateBook) -> Book:
        """
        Create a new book with provided details.
        """

        await get_by_title_author(self.db, payload.title, payload.author)
        book_data = payload.model_dump()
        book_data["slug"] = await generate_unique_slug(self.db, book_data['title'])
        book = Book(**book_data)
        self.db.add(book)
        await self.db.commit()
        await self.db.refresh(book)
        return book
    
    async def get_all_books(self) -> List[Book]:
        """
        Fetch all books added by users.
        """

        result = await self.db.execute(select(Book))
        return result.scalars().all()

    async def get_book(self, book_slug: str) -> Book:
        """
        Fetch book details based on slug.
        """

        result = await self.db.execute(select(Book).where(Book.slug == book_slug))
        book = result.scalar_one_or_none() 

        if not book:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=constants.BOOK_NOT_FOUND)
        return book

    async def update_book(self, book_slug: str, payload: UpdateBook) -> Book:
        """
        Update book details based on slug.
        """

        book = await self.get_book(book_slug)
        for key, value in payload.model_dump(exclude_unset=True).items():
            setattr(book, key, value)
        await self.db.commit()
        await self.db.refresh(book)
        return book

    async def delete_book(self, book_slug: str) -> None:
        """
        Delete book details based on slug.
        """

        book = await self.get_book(book_slug)
        await self.db.delete(book)
        await self.db.commit()
        return {"message": constants.BOOK_DELETED}
