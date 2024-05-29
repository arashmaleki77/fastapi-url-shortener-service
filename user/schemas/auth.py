from pydantic import BaseModel, constr, field_validator
from fastapi import HTTPException, status
import re
from user.schemas.user import UserSchema


class AuthBaseSchema(BaseModel):
    username: str

    @field_validator("username")
    def validate_username(cls, username: str) -> str:
        if len(username) < 5:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 5 characters long."
            )

        return username


class RegisterSchema(AuthBaseSchema):
    first_name: constr(max_length=25) = ""
    last_name: constr(max_length=25) = ""
    sub_directory: str
    password: str

    @field_validator("password")
    def validate_password(cls, password: str) -> str:
        if len(password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must be at least 8 characters long."
            )

        if not re.search(r"[A-Z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one uppercase character."
            )

        if not re.search(r"[a-z]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one lowercase character."
            )
        if not re.search(r"[0-9]", password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Password must contain at least one digit."
            )

        return password

    @field_validator("sub_directory")
    def validate_sub_directory(cls, sub_directory: str) -> str:
        constr(min_length=5, max_length=25)
        if len(sub_directory) < 5 or len(sub_directory) > 25:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Sub directory can have between 5 to 25 chars."
            )

        return sub_directory


class LoginSchema(AuthBaseSchema):
    password: constr(min_length=8)


class TokenSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserSchema


class SubDirectoryExistenceSchema(BaseModel):
    is_exists: bool
