from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class User(SQLModel, table=True):
    __tablename__ = "user"

    id: Optional[int] = Field(default=None, primary_key=True, index=True)
    username: str = Field(max_length=25, unique=True, index=True, nullable=False)
    sub_directory: str = Field(max_length=150, unique=True, index=True, nullable=False)
    first_name: str = Field(max_length=25, nullable=False)
    last_name: str = Field(max_length=25, nullable=False)
    password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False, sa_column_kwargs={"onupdate": datetime.utcnow}
    )
