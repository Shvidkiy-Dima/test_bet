from api.v1.event import router as event_router
from fastapi import APIRouter

api_router = APIRouter()
api_router.include_router(event_router, prefix="/api/v1/event")
