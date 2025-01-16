from datetime import datetime
from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.models.scheme import SchemeHistNavData
from app.schemas.scheme import SchemeHistNavDataSchema
from app.services.service import ReturnsCalculator, SchemeHistNavService
from app.db.base import get_db, get_idb
import logging
from sqlalchemy import select

from app.models.scheme import (
    Scheme,
    SchemeHolding,
    SchemeAudit,
    WSchemeCodeWPCMapping,
    ParentChildSchemeMapping,
    SectorToWSectorMapping,
    WPCToTWPCMapping,
    ISINWPCMapping,
    SchemeCodeWPCMapping
    # ...other models...
)
from app.schemas.scheme import (
    SchemeSchema,
    SchemeHoldingSchema,
    SchemeAuditSchema,
    WSchemeCodeWPCMappingSchema,
    SchemeCodeWPCMappingSchema,
    ParentChildSchemeMappingSchema,
    SectorToWSectorMappingSchema,
    WPCToTWPCMappingSchema,
    ISINWPCMappingSchema,
    ResolveResultSchema
    # ...other schemas...
)

router = APIRouter()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

@router.get("/{id_type}/{id_value}/returns", response_model=dict)
async def calculate_returns(
    request: Request, id_type: str, id_value: str, db: AsyncSession = Depends(get_idb)
):
    try:
        params = dict(request.query_params)
        params['id_type'] = id_type
        params['id_value'] = id_value
        rc = await ReturnsCalculator.create(params, db=db)
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

@router.get("/scheme/{wpc}/", response_model=SchemeSchema)
async def get_scheme(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching scheme for WPC: {wpc}")
    result = await db.execute(select(Scheme).where(Scheme.wpc == wpc))
    print(select(*[Scheme.wpc,Scheme.face_value]).where(Scheme.wpc == wpc))
    #result = await db.execute(select(*[Scheme.wpc,Scheme.face_value]).where(Scheme.wpc == wpc))
    result_list=list(result)
    scheme = result.scalar_one_or_none()
    if not scheme:
        logger.debug(f"No scheme found for WPC: {wpc}")
        raise HTTPException(status_code=404, detail="Scheme not found")
    return scheme

@router.get("/scheme-holdings/{wpc}/", response_model=List[SchemeHoldingSchema])
async def get_scheme_holdings(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching scheme holdings for WPC: {wpc}")
    result = await db.execute(select(SchemeHolding).where(SchemeHolding.wpc == wpc))
    holdings = result.scalars().all()
    if not holdings:
        logger.debug(f"No holdings found for WPC: {wpc}")
        return []
    return holdings

@router.get("/scheme-audit/{wpc}/", response_model=List[SchemeAuditSchema])
async def get_scheme_audit(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching scheme audit for WPC: {wpc}")
    result = await db.execute(select(SchemeAudit).where(SchemeAudit.wpc == wpc))
    audits = result.scalars().all()
    if not audits:
        logger.debug(f"No audits found for WPC: {wpc}")
        return []
    return audits

@router.get("/wscheme-code-wpc-mapping/{wpc}/", response_model=List[WSchemeCodeWPCMappingSchema])
async def get_wscheme_code_wpc_mapping(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching WSchemeCodeWPCMapping for WPC: {wpc}")
    result = await db.execute(select(WSchemeCodeWPCMapping).where(WSchemeCodeWPCMapping.wpc == wpc))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No WSchemeCodeWPCMapping found for WPC: {wpc}")
        return []
    return mappings

@router.get("/scheme-code-wpc-mapping/{wpc}/", response_model=List[SchemeCodeWPCMappingSchema])
async def get_scheme_code_wpc_mapping(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching SchemeCodeWPCMapping for WPC: {wpc}")
    result = await db.execute(select(SchemeCodeWPCMapping).where(SchemeCodeWPCMapping.wpc == wpc))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No SchemeCodeWPCMapping found for WPC: {wpc}")
        return []
    return mappings

@router.get("/parent-child-scheme-mapping/{wpc}/", response_model=List[ParentChildSchemeMappingSchema])
async def get_parent_child_scheme_mapping(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching ParentChildSchemeMapping for WPC: {wpc}")
    result = await db.execute(select(ParentChildSchemeMapping).where(ParentChildSchemeMapping.parent_wpc == wpc))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No ParentChildSchemeMapping found for WPC: {wpc}")
        return []
    return mappings

@router.get("/sector-to-wsector-mapping/{sector}/", response_model=List[SectorToWSectorMappingSchema])
async def get_sector_to_wsector_mapping(
    sector: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching SectorToWSectorMapping for WPC: {sector}")
    result = await db.execute(select(SectorToWSectorMapping).where(SectorToWSectorMapping.sector == sector))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No SectorToWSectorMapping found for WPC: {sector}")
        return []
    return mappings

@router.get("/wpctotwpcmapping/{wpc}/", response_model=List[WPCToTWPCMappingSchema])
async def get_wpctotwpc_mapping(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching WPCToTWPCMapping for WPC: {wpc}")
    result = await db.execute(select(WPCToTWPCMapping).where(WPCToTWPCMapping.wpc == wpc))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No WPCToTWPCMapping found for WPC: {wpc}")
        return []
    return mappings

@router.get("/isinwpcmapping/{wpc}/", response_model=List[ISINWPCMappingSchema])
async def get_isin_wpc_mapping(
    wpc: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching ISINWPCMapping for WPC: {wpc}")
    result = await db.execute(select(ISINWPCMapping).where(ISINWPCMapping.wpc == wpc))
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No ISINWPCMapping found for WPC: {wpc}")
        return []
    return mappings

