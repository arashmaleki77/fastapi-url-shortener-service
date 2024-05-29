from core.settings import settings
from core.database import Base, get_db
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from main import app
import pytest_asyncio
import pytest
from sqlalchemy.pool import NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


transport = ASGITransport(app=app)
settings.ENV = "test"
DATABASE_URL = settings.TEST_DATABASE_URI

engine = create_async_engine(DATABASE_URL, echo=True, poolclass=NullPool)
TestSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture(scope="function")
async def async_session():
    async with TestSessionLocal() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def async_client(async_session: AsyncSession):
    async def override_get_db():
        yield async_session

    app.dependency_overrides[get_db] = override_get_db
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client
    app.dependency_overrides[get_db] = get_db
