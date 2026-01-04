from uuid import UUID
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth.dependencies import verify_token
from users import schemas, services


router = APIRouter(prefix="/user")

@router.post("/", response_model=schemas.GetUser)
async def create_user(payload: schemas.CreateUser, db:AsyncSession = Depends(get_db)):
    service = services.UserService(db)
    return await service.register_user(payload)

@router.get("/{user_id}/", response_model=schemas.GetUser)
async def get_user(user_id:UUID, auth_user: None = Depends(verify_token), db:AsyncSession = Depends(get_db)):
    service = services.UserService(db)
    return await service.get_user(user_id)