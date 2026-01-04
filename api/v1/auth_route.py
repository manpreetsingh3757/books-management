
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from auth import schemas as auth_schemas, services

router = APIRouter(prefix="/auth")

@router.post("/login/", response_model=auth_schemas.LoginToken)
async def create_user(payload: auth_schemas.LoginUser, db:AsyncSession = Depends(get_db)):
    service = services.AuthService(db)
    return await service.login_user(payload)
