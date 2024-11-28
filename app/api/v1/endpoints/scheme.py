from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.schemas.scheme import SchemeHistNavData
from app.services.service import ReturnsCalculator,SchemeHistNavService
from app.deps import get_db

router = APIRouter()

@router.get("/{id_type}/{id_value}/returns", response_model=dict)
async def calculate_returns(
    id_type: str,
    id_value: str,
    db: AsyncSession = Depends(get_db)
):
    params = {
        'id_type': id_type,
        'id_value': id_value
    }
    returns = await ReturnsCalculator.calculate_returns(db, params)
    return returns