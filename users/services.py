from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from auth.helper import hash_password
from users import schemas
from users import constants
from users.models import User


class UserService:
    """
    User based services
    """
    def __init__(self, db: AsyncSession):
        self.db = db

    async def register_user(self, payload: schemas.CreateUser) -> User:
        """
        Create a new user based on enterd details
        """

        user = User(
            email=payload.email,
            password=hash_password(payload.password),
        )
        self.db.add(user)
        try:
            await self.db.commit()
            await self.db.refresh(user)
        except IntegrityError as e:
            await self.db.rollback()
            if "email" in str(e.orig):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"User with email '{payload.email}' already exists"
                )
            raise e
        except Exception as e:
            await self.db.rollback()
            raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )
        return user
    
    async def get_user(self, user_id: UUID) -> User:
        """
        Get user details based on selected user id
        """

        user = await self.db.get(User, user_id)

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=constants.USER_NOT_FOUND
            )
        return user