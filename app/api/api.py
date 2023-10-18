from fastapi import APIRouter

from app.api.routes import user, entry

api_router = APIRouter()
api_router.include_router(user.router, prefix="/users")
api_router.include_router(entry.router, prefix="/entry")
# api_router.include_router(check.router, prefix="/check")