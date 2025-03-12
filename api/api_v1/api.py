from fastapi import APIRouter

from api.api_v1.endpoints import categories, listingss, login
from api.api_v1.endpoints import users

api_router = APIRouter()
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(login.router, prefix="/login", tags=["login"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(listingss.router, prefix="/listingss", tags=["listingss"])
