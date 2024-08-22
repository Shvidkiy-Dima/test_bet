from database import engine
from sqlalchemy.ext.asyncio import AsyncSession


async def get_db():
    session = AsyncSession(bind=engine, expire_on_commit=False)
    try:
        yield session
    finally:
        await session.close()
