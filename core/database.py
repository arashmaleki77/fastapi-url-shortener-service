from sys import modules
from sqlalchemy.orm import declarative_base, sessionmaker
from core.settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


DATABASE_URI = settings.DATABASE_URI
if "pytest" in modules:
    DATABASE_URI = settings.TEST_DATABASE_URI


engine = create_async_engine(DATABASE_URI, echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()


async def get_db() -> AsyncSession:
    async with SessionLocal() as session:
        yield session
