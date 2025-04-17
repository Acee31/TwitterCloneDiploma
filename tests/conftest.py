import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from app.db.base_model import Base
from app.db.db_settings import db_session as db
from app.main import app
from app.routes.crud.insert_data import insert_data

test_db_url = "sqlite+aiosqlite:///:memory:"
test_engine = create_async_engine(url=test_db_url, echo=False)
test_async_session = sessionmaker(
    bind=test_engine, class_=AsyncSession, expire_on_commit=False
)


@pytest_asyncio.fixture()
async def create_db():
    """
    Creates and initializes a test database in memory.
    Creates all tables, populates them with initial data,
    and deletes the tables after the tests are complete
    """

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with test_async_session() as session:
        await insert_data(session)

    yield test_engine

    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture()
async def db_session(create_db):
    """
    Creates a session to work with the database within the test
    """

    async with test_async_session() as session:
        yield session


@pytest_asyncio.fixture()
async def client(db_session):
    """
    Creates an HTTP client for testing a FastAPI application.
    Redefines the dependency of getting a database session to a test one
    """

    async def override_get_session():
        yield db_session

    app.dependency_overrides[db.get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client
