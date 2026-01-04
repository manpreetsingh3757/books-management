from sqlalchemy import String, Integer, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from core.database import Base


class Book(Base):
    __tablename__ = "books"
    
    id: Mapped[int] = mapped_column(primary_key=True,index=True)
    title: Mapped[str] = mapped_column(String(255),nullable=False)
    author: Mapped[str] = mapped_column(String(255),nullable=False)
    genre: Mapped[str] = mapped_column(String(255),nullable=False)
    year_published: Mapped[int] = mapped_column(Integer,nullable=False)
    summary: Mapped[str | None] = mapped_column(Text,nullable=True)
    slug: Mapped[str] = mapped_column(String(300),unique=True,index=True,nullable=False)

    reviews = relationship("Review", back_populates="book", cascade="all, delete-orphan" )

