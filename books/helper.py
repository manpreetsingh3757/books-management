from fastapi import HTTPException, status
from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from books.models import Book
from books import constants


async def get_by_title_author(db: AsyncSession, title: str, author: str) -> Book | None:
    """
    Check whether a book with the given title and author already exists.
    """

    stmt = select(Book).where(Book.title == title, Book.author == author)
    result = await db.execute(stmt)
    existing =  result.scalar_one_or_none()
    if existing:
        raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail=constants.SAME_BOOK_EXIST
                    )

async def generate_unique_slug(db: AsyncSession, title: str) -> str:
    """
    Generate a unique slug for each book.
    """

    base_slug = slugify(title)
    slug = base_slug
    counter = 1

    while True:
        result = await db.execute(
            select(Book).where(Book.slug == slug)
        )
        existing = result.scalar_one_or_none()

        if not existing:
            return slug

        slug = f"{base_slug}-{counter}"
        counter += 1
