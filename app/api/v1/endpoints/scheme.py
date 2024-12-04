from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.scheme import SchemeHistNavData
from app.schemas.scheme import SchemeHistNavDataSchema
from app.services.service import ReturnsCalculator,SchemeHistNavService
from app.db.base import get_db, get_idb
import logging

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)
@router.get("/{id_type}/{id_value}/returns", response_model=dict)
async def calculate_returns(
    request: Request, id_type: str, id_value: str, db: AsyncSession = Depends(get_db)
):
    try:
        params = dict(request.query_params)
        params['id_type'] = id_type
        params['id_value'] = id_value
        rc = ReturnsCalculator(data=params)
        returns = await rc.calculate_returns(db)
        return returns
    except Exception as e:
        logger.error(f"Error in calculate_returns: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/get-scheme-hist-nav/{wpc}/", response_model=List[SchemeHistNavDataSchema])
async def get_scheme_hist_nav_data(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching historical NAV data for WPC: {wpc}")
    records = await SchemeHistNavService.get_hist_nav_data(db, wpc)
    if records is None:
        logger.debug(f"No records found for WPC: {wpc}")
        return []
    logger.debug(f"Records found for WPC: {wpc}: {records}")
    return [records] if not isinstance(records, list) else records
