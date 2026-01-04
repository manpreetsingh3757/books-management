import uuid
import enum
from sqlalchemy import String, Boolean, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class UserRole(str, enum.Enum):
    CLIENT = "client"

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255),unique=True,index=True,nullable=False)
    password: Mapped[str] = mapped_column(String(255),nullable=False)
    role: Mapped[UserRole] = mapped_column(Enum(UserRole, name="user_role_enum"),nullable=False,default=UserRole.CLIENT)
    is_active: Mapped[bool] = mapped_column(Boolean,nullable=False,default=True)

    reviews = relationship("Review", back_populates="user", lazy="dynamic")