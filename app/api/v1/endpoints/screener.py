from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import get_idb
from app.services.screener import ScreenerService
from typing import List
from app.schemas.screener import ScreenerResponse, ScreenerWithInstrumentsResponse

router = APIRouter()

@router.get("/screeners/{screener_wpc}", response_model=ScreenerResponse)
async def get_screener_by_wpc(screener_wpc: str, db: AsyncSession = Depends(get_idb)):
    """
    Retrieve a screener by its WPC.
    """
    screener = await ScreenerService.get_screener_by_wpc(db, screener_wpc)
    if not screener:
        raise HTTPException(status_code=404, detail="Screener not found")
    return screener

@router.get("/screeners/{screener_wpc}/instruments", response_model=ScreenerWithInstrumentsResponse)
async def get_screener_with_instruments(screener_wpc: str, db: AsyncSession = Depends(get_idb)):
    """
    Retrieve a screener and its instruments by screener WPC.
    """
    screener_with_instruments = await ScreenerService.get_screener_with_instruments(db, screener_wpc)
    if not screener_with_instruments:
        raise HTTPException(status_code=404, detail="Screener not found")
    return screener_with_instruments

# Add more endpoints as needed

# Make sure to export the router
__all__ = ["router"]
