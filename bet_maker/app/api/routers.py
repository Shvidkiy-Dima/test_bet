from api.v1.bet import router as bet_router
from api.v1.callback import router as callback_router
from api.v1.event import router as event_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(bet_router, prefix="/api/v1/bet")
api_router.include_router(event_router, prefix="/api/v1/event")
api_router.include_router(callback_router, prefix="/api/v1/callback", include_in_schema=False)
