from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.helper import verify_password, create_access_token
from auth import schemas, constants
from users.models import User

class AuthService:
    
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login_user(self, payload: schemas.LoginUser) -> schemas.LoginToken:
        """
        Authenticate the user using email and password and return an access token.
        """

        stmt = select(User).where(User.email == payload.email)
        result = await self.db.execute(stmt)
        user: User | None = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=constants.INVALID_EMAIL
            )

        if not verify_password(payload.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=constants.INVALID_PASSWORD
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=constants.USER_INACTIVE
            )

        access_token = create_access_token(subject=str(user.id))

        return schemas.LoginToken(
            access_token=access_token,
            token_type="bearer"
        )