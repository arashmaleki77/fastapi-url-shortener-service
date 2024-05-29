from fastapi import Depends, HTTPException, status, Security
from core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from user.auth.auth import decode_access_token
from user.crud.user import get_user
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer


security = HTTPBearer()


async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Security(security),
        db: AsyncSession = Depends(get_db)
):
    token = credentials.credentials
    payload = decode_access_token(token)
    user_id: int = payload.get("subject")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await get_user(db=db, user_id=user_id)
    return user
