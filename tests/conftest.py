import pytest
import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.main import app
from src.models.trade_result import Base, TradeResult
from src.config import settings
from .fixtures.postgres.trade_results import TRADE_RESULTS


engine = create_async_engine(settings.DATABASE_URL)
SESSION_FACTORY = async_sessionmaker(bind=engine)


@pytest_asyncio.fixture
async def test_client():
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport, base_url=settings.HOST
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_db(get_test_data):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with SESSION_FACTORY() as session:
        session.add_all(get_test_data)
        await session.commit()

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def get_test_data():
    return [TradeResult(**trade_result) for trade_result in TRADE_RESULTS]
