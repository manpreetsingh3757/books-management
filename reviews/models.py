import uuid
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base

class Review(Base):
    __tablename__ = "reviews"

    id: Mapped[int] = mapped_column(primary_key=True)
    book_id: Mapped[int] = mapped_column(ForeignKey("books.id", ondelete="CASCADE"))
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),ForeignKey("users.id"))
    review_text: Mapped[str] = mapped_column(Text)
    rating: Mapped[int] = mapped_column(Integer)

    book = relationship("Book", back_populates="reviews")
    user = relationship("User", back_populates="reviews")
