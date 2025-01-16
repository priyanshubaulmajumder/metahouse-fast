from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.stock import StockResponse, PaginatedStockResponse, StockFundamentalsResponse, ShareHoldingPatternResponse, FinancialsOverviewResponse, DetailedFinancialsResponse
from app.services.stock import StockService
from app.db.base import get_db, get_idb
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.stock import (
    Stock,
    StockNSEHistPriceData,
    StockBSEHistPriceData,
    StockManagementInfo,
    StockWCategoryMapping,
    StockIDWPCMapping,
    StockYearlyRatioHistData,
    StockShareHoldingHistData,
    StockBonusHistData,

    StockRightsHistData,
    StockBoardMeetingHistData,
    StockFinancialQuarterlyResult,
    StockFinancialHalfYearlyResult,
    StockFinancialNineMonthResult,
    StockFinancialYearlyResult,
    StockBalanceSheet,
    StockBalanceSheetQuarterly,
)
from app.schemas.stock import (
    StockSchema,
    StockNSEHistPriceDataSchema,
    StockBSEHistPriceDataSchema,
    StockManagementInfoSchema,
    StockWCategoryMappingSchema,
    StockIDWPCMappingSchema,
    StockYearlyRatioHistDataSchema,
    StockShareHoldingHistDataSchema,
    StockBonusHistDataSchema,
    StockRightsHistDataSchema,
    StockBoardMeetingHistDataSchema,
    StockFinancialQuarterlyResultSchema,
    StockFinancialHalfYearlyResultSchema,
    StockFinancialNineMonthResultSchema,
    StockFinancialYearlyResultSchema,
    StockBalanceSheetSchema,
    StockBalanceSheetQuarterlySchema,
    StockBalanceSheetHalfYearlySchema,
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/stock/{wstockcode}/", response_model=StockSchema)
async def get_stock(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching stock for wstockcode: {wstockcode}")
    result = await db.execute(select(Stock).where(Stock.wstockcode == wstockcode))
    stock = result.scalar_one_or_none()
    if not stock:
        logger.debug(f"No stock found for wstockcode: {wstockcode}")
        raise HTTPException(status_code=404, detail="Stock not found")
    logger.debug(f"Stock found: {stock}")
    return stock




@router.get("/stock-nse-hist-price/{wstockcode}/", response_model=List[StockNSEHistPriceDataSchema])
async def get_stock_nse_hist_price_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching NSE historical price data for wstockcode: {wstockcode}")
    result = await db.execute(select(StockNSEHistPriceData).where(StockNSEHistPriceData.wstockcode == wstockcode))
    records = result.scalars().all()
    if not records:
        logger.debug(f"No NSE historical price data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Records found: {len(records)}")
    return records

@router.get("/stock-bse-hist-price/{wstockcode}/", response_model=List[StockBSEHistPriceDataSchema])
async def get_stock_bse_hist_price_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching BSE historical price data for wstockcode: {wstockcode}")
    result = await db.execute(select(StockBSEHistPriceData).where(StockBSEHistPriceData.wstockcode == wstockcode))
    records = result.scalars().all()
    if not records:
        logger.debug(f"No BSE historical price data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Records found: {len(records)}")
    return records

@router.get("/stock-management-info/{wstockcode}/", response_model=StockManagementInfoSchema)
async def get_stock_management_info(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching management info for wstockcode: {wstockcode}")
    result = await db.execute(select(StockManagementInfo).where(StockManagementInfo.wstockcode == wstockcode))
    info = result.scalar_one_or_none()
    if not info:
        logger.debug(f"No management info found for wstockcode: {wstockcode}")
        raise HTTPException(status_code=404, detail="Management info not found")
    logger.debug(f"Management info found: {info}")
    return info

@router.get("/stock-wcategory-mapping/{wstockcode}/", response_model=StockWCategoryMappingSchema)
async def get_stock_wcategory_mapping(
    token: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching category mapping for wstockcode: {token}")
    result = await db.execute(select(StockWCategoryMapping).where(StockWCategoryMapping.token == token))
    mapping = result.scalar_one_or_none()
    if not mapping:
        logger.debug(f"No category mapping found for wstockcode: {token}")
        raise HTTPException(status_code=404, detail="Category mapping not found")
    logger.debug(f"Category mapping found: {mapping}")
    return mapping

@router.get("/stock-id-wpc-mapping/{wstockcode}/", response_model=List[StockIDWPCMappingSchema])
async def get_stock_id_wpc_mapping(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching ID to WPC mappings for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockIDWPCMapping).where(StockIDWPCMapping.wstockcode == wstockcode)
    )
    mappings = result.scalars().all()
    if not mappings:
        logger.debug(f"No ID to WPC mappings found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(mappings)} mappings")
    return mappings

@router.get("/stock-yearly-ratio-hist-data/{wstockcode}/", response_model=List[StockYearlyRatioHistDataSchema])
async def get_stock_yearly_ratio_hist_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching yearly ratio history data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockYearlyRatioHistData).where(StockYearlyRatioHistData.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No yearly ratio history data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-share-holding-hist-data/{wstockcode}/", response_model=List[StockShareHoldingHistDataSchema])
async def get_stock_share_holding_hist_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching share holding history data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockShareHoldingHistData).where(StockShareHoldingHistData.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No share holding history data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-bonus-hist-data/{wstockcode}/", response_model=List[StockBonusHistDataSchema])
async def get_stock_bonus_hist_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching bonus history data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockBonusHistData).where(StockBonusHistData.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No bonus history data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records


@router.get("/stock-rights-hist-data/{wstockcode}/", response_model=List[StockRightsHistDataSchema])
async def get_stock_rights_hist_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching rights history data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockRightsHistData).where(StockRightsHistData.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No rights history data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-board-meeting-hist-data/{wstockcode}/", response_model=List[StockBoardMeetingHistDataSchema])
async def get_stock_board_meeting_hist_data(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching board meeting history data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockBoardMeetingHistData).where(StockBoardMeetingHistData.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No board meeting history data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-financial-quarterly-result/{wstockcode}/", response_model=List[StockFinancialQuarterlyResultSchema])
async def get_stock_financial_quarterly_result(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching financial quarterly results for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockFinancialQuarterlyResult).where(StockFinancialQuarterlyResult.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No financial quarterly results found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-financial-half-yearly-result/{wstockcode}/", response_model=List[StockFinancialHalfYearlyResultSchema])
async def get_stock_financial_half_yearly_result(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching financial half-yearly results for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockFinancialHalfYearlyResult).where(StockFinancialHalfYearlyResult.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No financial half-yearly results found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-financial-nine-month-result/{wstockcode}/", response_model=List[StockFinancialNineMonthResultSchema])
async def get_stock_financial_nine_month_result(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching financial nine-month results for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockFinancialNineMonthResult).where(StockFinancialNineMonthResult.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No financial nine-month results found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-financial-yearly-result/{wstockcode}/", response_model=List[StockFinancialYearlyResultSchema])
async def get_stock_financial_yearly_result(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching financial yearly results for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockFinancialYearlyResult).where(StockFinancialYearlyResult.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No financial yearly results found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-balance-sheet/{wstockcode}/", response_model=List[StockBalanceSheetSchema])
async def get_stock_balance_sheet(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching balance sheet data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockBalanceSheet).where(StockBalanceSheet.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No balance sheet data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-balance-sheet-quarterly/{wstockcode}/", response_model=List[StockBalanceSheetQuarterlySchema])
async def get_stock_balance_sheet_quarterly(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching quarterly balance sheet data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockBalanceSheetQuarterly).where(StockBalanceSheetQuarterly.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No quarterly balance sheet data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

@router.get("/stock-balance-sheet-half-yearly/{wstockcode}/", response_model=List[StockBalanceSheetHalfYearlySchema])
async def get_stock_balance_sheet_half_yearly(
    wstockcode: str, db: AsyncSession = Depends(get_idb)
):
    logger.debug(f"Fetching half-yearly balance sheet data for wstockcode: {wstockcode}")
    result = await db.execute(
        select(StockBalanceSheetHalfYearly).where(StockBalanceSheetHalfYearly.wstockcode == wstockcode)
    )
    records = result.scalars().all()
    if not records:
        logger.debug(f"No half-yearly balance sheet data found for wstockcode: {wstockcode}")
        return []
    logger.debug(f"Found {len(records)} records")
    return records

'''
@router.get("/search", response_model=PaginatedStockResponse)
def stock_search(
    text: str,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    stocks, total = StockService.search_stocks(db, text, skip, limit)
    return {
        "items": stocks,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{id_type}/{id_value}/historical", response_model=List[dict])
def get_stock_historical_prices(
    id_type: str,
    id_value: str,
    exchange: str = Query(..., description="Stock exchange"),
    start_date: str = Query(..., description="Start date in YYYY-MM-DD format"),
    end_date: str = Query(..., description="End date in YYYY-MM-DD format"),
    db: Session = Depends(get_db)
):
    historical_prices = StockService.get_stock_historical_price(db, id_type, id_value, exchange, start_date, end_date)
    return historical_prices

@router.get("/news", response_model=List[dict])
def get_stock_market_news(
    news_type: str = Query(..., description="News type: 'sn' for stock news, 'mn' for market news"),
    db: Session = Depends(get_db)
):
    news = StockService.get_stock_market_news(db, news_type)
    return news

@router.get("/news/{news_id}", response_model=dict)
def get_stock_market_specific_news(
    news_id: str,
    db: Session = Depends(get_db)
):
    news = StockService.get_stock_market_specific_news(db, news_id)
    return news

@router.get("/etfs", response_model=List[dict])
def get_etfs(
    fund_types: List[str] = Query(..., description="List of fund types"),
    db: Session = Depends(get_db)
):
    etfs = StockService.get_etfs(db, fund_types)
    return etfs

@router.get("/{id_type}/{id_value}/similar-etfs", response_model=List[dict])
def get_similar_etfs(
    id_type: str,
    id_value: str,
    db: Session = Depends(get_db)
):
    similar_etfs = StockService.get_similar_etfs(db, id_type, id_value)
    return similar_etfs

@router.get("/indices", response_model=List[dict])
def get_indices(
    category: str = Query(..., description="Index category"),
    db: Session = Depends(get_db)
):
    indices = StockService.get_stock_indices_for_category(db, category)
    return indices

@router.get("/indices/{id_type}/{id_value}/stocks", response_model=PaginatedStockResponse)
def get_index_wise_stocks(
    id_type: str,
    id_value: str,
    skip: int = 0,
    limit: int = 500,
    db: Session = Depends(get_db)
):
    stocks, total = StockService.get_index_wise_stocks(db, id_type, id_value, skip, limit)
    return {
        "items": stocks,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{id_type}/{id_value}/fundamentals", response_model=StockFundamentalsResponse)
def get_stock_fundamentals(
    id_type: str,
    id_value: str,
    exchange: str = Query(..., description="Stock exchange"),
    db: Session = Depends(get_db)
):
    fundamentals = StockService.get_stock_fundamentals(db, id_type, id_value, exchange)
    return fundamentals

@router.get("/{id_type}/{id_value}/share-holdings-pattern", response_model=ShareHoldingPatternResponse)
def get_share_holding_pattern(
    id_type: str,
    id_value: str,
    entity: str = Query(..., description="Entity type"),
    db: Session = Depends(get_db)
):
    pattern = StockService.get_latest_share_holding_pattern(db, id_type, id_value, entity)
    return pattern

@router.get("/{id_type}/{id_value}/financials-overview", response_model=FinancialsOverviewResponse)
def get_financials_overview(
    id_type: str,
    id_value: str,
    fdata: str = Query(..., description="Financial data type"),
    period: str = Query(..., description="Period"),
    rtype: str = Query(..., description="Report type"),
    db: Session = Depends(get_db)
):
    overview = StockService.get_financial_data_overview(db, id_type, id_value, fdata, period, rtype)
    return overview

@router.get("/{id_type}/{id_value}/financials", response_model=DetailedFinancialsResponse)
def get_detailed_financials(
    id_type: str,
    id_value: str,
    period: str = Query(..., description="Period"),
    rtype: str = Query(..., description="Report type"),
    db: Session = Depends(get_db)
):
    financials = StockService.get_financial_data_detailed(db, id_type, id_value, period, rtype)
    return financials

@router.get("/{id_type}/{id_value}/technical-indicators", response_model=dict)
async def get_stock_technical_indicators(
    id_type: str,
    id_value: str,
    db: AsyncSession = Depends(get_db)
):
    indicators = await StockService.get_stock_technical_indicators(db, id_type, id_value)
    return indicators

@router.get("/{id_type}/{id_value}/returns", response_model=dict)
async def get_stock_returns(
    id_type: str,
    id_value: str,
    db: AsyncSession = Depends(get_db)
):
    returns = await StockService.get_stock_returns(db, id_type, id_value)
    return returns
'''