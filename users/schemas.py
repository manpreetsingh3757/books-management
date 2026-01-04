
import uuid
from pydantic import BaseModel, Field, EmailStr
from users.models import UserRole

class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=255)
    role: UserRole = Field(default=UserRole.CLIENT)

class CreateUser(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

class GetUser(UserBase):
    id: uuid.UUID
    is_active: bool = True

    model_config = {
        "from_attributes": True
    }
