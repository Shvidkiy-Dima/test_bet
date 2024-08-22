from contextlib import asynccontextmanager

import uvicorn
from api.routers import api_router
from event_manager import EventManager
from fastapi import FastAPI
from settings import settings


@asynccontextmanager
async def app_lifespan(app: FastAPI):
    await EventManager.start()
    yield

    await EventManager.stop()


def get_app() -> FastAPI:
    fast_api = FastAPI(lifespan=app_lifespan)
    fast_api.include_router(api_router)
    return fast_api


app = get_app()


if __name__ == "__main__":
    uvicorn.run(
        app,
        host=settings.HOST,
        port=settings.PORT,
    )
