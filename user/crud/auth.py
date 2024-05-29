from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from user.models.user import User


async def get_sub_directory_existence(db: AsyncSession, sub_directory: str):
    result = await db.execute(select(User).filter(User.sub_directory == sub_directory))
    return bool(result.scalars().first())
