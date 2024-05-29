from sqlalchemy import UniqueConstraint, Index
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from user.models.user import User


class ShortenerURL(SQLModel, table=True):
    __tablename__ = "shortener_url"
    __table_args__ = (
        UniqueConstraint("short_url", "user_id", name="unique_short_url_user_id"),
        Index("index_short_url_user_id", "short_url", "user_id")
    )

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    short_url: str = Field(max_length=5, nullable=False, index=True)
    original_url: str = Field(nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user: Optional["User"] = Relationship(
        sa_relationship_kwargs={
            "lazy": "joined",
            "primaryjoin": "ShortenerURL.user_id==User.id",
        }
    )
