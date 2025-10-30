from fastapi import APIRouter
from app.api.v1 import auth, points, images, admin, export

api_router = APIRouter()

api_router.include_router(auth.router, tags=["Authentication"])
api_router.include_router(points.router, prefix="/points", tags=["Pollution Points"])
api_router.include_router(images.router, prefix="/images", tags=["Images"])
api_router.include_router(admin.router, prefix="/admin", tags=["Admin"])
api_router.include_router(export.router, prefix="/export", tags=["Export"])