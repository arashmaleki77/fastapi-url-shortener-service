from sqlalchemy.ext.asyncio import AsyncSession
from user.schemas.auth import RegisterSchema
from sqlalchemy.future import select
from user.auth.auth import get_hashed_password
from user.models.user import User


async def get_user(db: AsyncSession, user_id: int):
    result = await db.execute(select(User).filter(User.id == int(user_id)))
    return result.scalars().first()


async def get_user_by_sub_directory(db: AsyncSession, sub_directory: str):
    result = await db.execute(select(User).filter(User.sub_directory == sub_directory))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str):
    result = await db.execute(select(User).filter(User.username == username))
    return result.scalars().first()


async def create_user(db: AsyncSession, current_user: RegisterSchema):
    hashed_password = get_hashed_password(current_user.password)
    new_user = User(
        username=current_user.username,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        password=hashed_password,
        sub_directory=current_user.sub_directory
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user
