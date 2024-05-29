from pydantic import BaseModel, computed_field, field_validator, ConfigDict
from datetime import datetime
from core.settings import settings
from user.schemas.user import UserSchema
import re
from fastapi import HTTPException, status


class BaseShortenerUrlSchema(BaseModel):
    original_url: str


class ShortenerUrlSchema(BaseShortenerUrlSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    short_url: str
    user: UserSchema
    created_at: datetime

    @computed_field
    @property
    def full_short_url(self) -> str:
        return f"{settings.FRONT_END_URL}/{self.user.sub_directory}/{self.short_url}"


class CreateShortenerUrlSchema(BaseShortenerUrlSchema):
    model_config = ConfigDict(from_attributes=True)

    @field_validator("original_url")
    def validate_url(cls, original_url: str) -> str:
        regex = re.compile(
            r'^(?:http|ftp)s?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # ...or ipv4
            r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # ...or ipv6
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)

        if not re.match(regex, original_url):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid URL")

        return original_url
