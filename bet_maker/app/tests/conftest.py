import sys
from pathlib import Path

app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir))

import pytest_asyncio
from api.dependences import get_db
from loguru import logger
from main import app
from models.base import Base
from settings import settings
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine


@pytest_asyncio.fixture
async def session():
    engine = create_async_engine(f"{settings.DB_URL}")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

        session = AsyncSession(bind=engine, expire_on_commit=False)
        app.dependency_overrides[get_db] = lambda: session
        yield session
    except Exception as e:
        raise e
    finally:
        await session.close()
        async with engine.begin() as conn:
            try:
                await conn.run_sync(Base.metadata.drop_all)
            except Exception as e:
                logger.exception(e)
        await engine.dispose()
