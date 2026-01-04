from fastapi import status
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.dependencies import verify_token
from books import schemas, services


router = APIRouter(prefix="/books")

@router.post("/", response_model=schemas.GetBook, status_code=status.HTTP_201_CREATED)
async def create_book(payload: schemas.CreateBook, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.BookService(db)
    return await service.create_book(payload)

@router.get("/", response_model=list[schemas.GetBook])
async def get_books(auth_user: None = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    service = services.BookService(db)
    return await service.get_all_books()

@router.get("/{book_slug}/", response_model=schemas.GetBook)
async def get_book(book_slug: str, auth_user: None = Depends(verify_token), db: AsyncSession = Depends(get_db)):
    service = services.BookService(db)
    return await service.get_book(book_slug)

@router.put("/{book_slug}/")
async def update_book(book_slug: str, payload: schemas.UpdateBook, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.BookService(db)
    return await service.update_book(book_slug, payload)

@router.delete("/{book_slug}/")
async def delete_book(book_slug: str, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.BookService(db)
    return await service.delete_book(book_slug)
