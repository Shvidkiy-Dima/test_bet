from settings import settings
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(settings.DB_URL)
