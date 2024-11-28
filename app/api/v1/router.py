from fastapi import APIRouter
from app.api.v1.endpoints import scheme, screener, stock

api_router = APIRouter()

api_router.include_router(stock.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(screener.router, prefix="/screener", tags=["screener"])
api_router.include_router(scheme.router, prefix="/scheme", tags=["scheme"])
# Add more routers as needed

# Add this line to export api_router
__all__ = ["api_router"]
