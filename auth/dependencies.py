from uuid import UUID
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from core.database import get_db
from core.config import settings
from users.models import User
from auth import constants

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def verify_token(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db),) -> User:    
    """
    Dependency to verify whether the user is authenticated before performing any operation.
    """

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )

        user_id: str | None = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=constants.INVALID_AUTH_TOKEN,
            )

        user_uuid = UUID(user_id)

    except (JWTError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.INVALID_AUTH_TOKEN,
        )

    user = await db.get(User, user_uuid)

    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=constants.INACTIVE_USER,
        )

    return user
