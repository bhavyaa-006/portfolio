from fastapi import APIRouter
from app.api.routers import auth, portfolio

api_router = APIRouter()
api_router.include_router(auth.router, tags=["login"])
api_router.include_router(portfolio.router, prefix="/portfolio", tags=["portfolio"])
