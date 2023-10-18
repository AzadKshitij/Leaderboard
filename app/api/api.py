from fastapi import APIRouter

from app.api.routes import user, event,check

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users")
api_router.include_router(event.router, prefix="/events")
api_router.include_router(check.router, prefix="/check")