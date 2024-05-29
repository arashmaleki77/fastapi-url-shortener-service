from fastapi import APIRouter, Depends
from user.dependencies import get_current_user
from user.schemas.user import UserSchema


user_router = APIRouter(prefix="/user", tags=["user"])


@user_router.get("/info/", response_model=UserSchema)
async def get_user_info(current_user: UserSchema = Depends(get_current_user)):
    return current_user
