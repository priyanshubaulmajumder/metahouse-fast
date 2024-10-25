from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.deps import get_db
from app.services.screener_service import ScreenerService
from typing import List
from app.schemas.screener_schemas import ScreenerResponse

router = APIRouter()

@router.get("/", response_model=List[ScreenerResponse])
async def get_screeners(db: AsyncSession = Depends(get_db)):
    return await ScreenerService.get_screeners(db)

@router.get("/{screener_id}", response_model=ScreenerResponse)
async def get_screener(screener_id: str, db: AsyncSession = Depends(get_db)):
    return await ScreenerService.get_screener(db, screener_id)

# Add more endpoints as needed

# Make sure to export the router
__all__ = ["router"]
