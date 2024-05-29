from fastapi import APIRouter, Depends, HTTPException, status
from user.crud.auth import get_sub_directory_existence
from user.crud.user import get_user_by_username, create_user
from user.schemas.auth import LoginSchema, RegisterSchema, TokenSchema, SubDirectoryExistenceSchema
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from user.auth.auth import create_access_token, verify_password


auth_router = APIRouter(prefix="/auth", tags=["registration"])


@auth_router.post("/register/", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def register(user: RegisterSchema, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    new_user = await create_user(db=db, current_user=user)

    access_token = create_access_token(user_id=new_user.id)
    return {"access_token": access_token, "user": new_user}
    # return TokenSchema(access_token=access_token, user=new_user)


@auth_router.post("/login/", response_model=TokenSchema, status_code=status.HTTP_200_OK)
async def login(current_user: LoginSchema, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(db, username=current_user.username)

    if not db_user or not verify_password(current_user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid username or password")

    access_token = create_access_token(user_id=db_user.id)
    return {"access_token": access_token, "user": db_user}
    # return TokenSchema(access_token=access_token, user=db_user)


@auth_router.get("/check-if-sub-directory-exists/", response_model=SubDirectoryExistenceSchema)
async def check_if_sub_directory_exists(sub_directory, db: AsyncSession = Depends(get_db)):
    is_sub_directory_exists = await get_sub_directory_existence(db, sub_directory)
    return {"is_exists": is_sub_directory_exists}
    # return SubDirectoryExistenceSchema(is_exists=is_sub_directory_exists)
