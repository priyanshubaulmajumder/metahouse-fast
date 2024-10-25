from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.stock_schemas import StockResponse, PaginatedStockResponse, StockFundamentalsResponse, ShareHoldingPatternResponse, FinancialsOverviewResponse, DetailedFinancialsResponse
from app.services.stock_service import StockService
from app.deps import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

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
