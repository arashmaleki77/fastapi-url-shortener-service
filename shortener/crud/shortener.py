from shortener.models.shortener import ShortenerURL
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from shortener.utils import generate_short_url


async def get_long_url_by_shortener_url(db: AsyncSession, user_id: int, short_url: str):
    result = await db.execute(select(ShortenerURL).filter(
        ShortenerURL.user_id == user_id, ShortenerURL.short_url == short_url)
    )
    return result.scalars().first()


async def create_shortener_url(db: AsyncSession, original_url: str, user_id: int):
    for index in range(5):
        try:
            short_url = generate_short_url()
            new_shortener_url = ShortenerURL(
                short_url=short_url,
                user_id=user_id,
                original_url=original_url
            )
            db.add(new_shortener_url)
            await db.commit()
            await db.refresh(new_shortener_url)
            return new_shortener_url
        except Exception as error:
            print(error)
    return None


async def get_shortener_url_by_id(db: AsyncSession, user_id: int, pk: int):
    result = await db.execute(select(ShortenerURL).filter(
        ShortenerURL.id == pk, ShortenerURL.user_id == user_id)
    )
    return result.scalars().first()


async def get_shortener_urls_by_user_id(db: AsyncSession, user_id: int):
    result = await db.execute(select(ShortenerURL).filter(ShortenerURL.user_id == user_id))
    return result.all()
