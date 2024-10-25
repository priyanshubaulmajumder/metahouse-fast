from fastapi import APIRouter
from app.api.v1.endpoints import stock_api, screener_api, scheme_api

api_router = APIRouter()

api_router.include_router(stock_api.router, prefix="/stocks", tags=["stocks"])
api_router.include_router(screener_api.router, prefix="/screener", tags=["screener"])
#api_router.include_router(scheme_api.router, prefix="/scheme", tags=["scheme"])
# Add more routers as needed

# Add this line to export api_router
__all__ = ["api_router"]
