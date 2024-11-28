import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.stock import Stock, StockNSEHistPriceData, StockBSEHistPriceData
from tests.test_data.stock_test_data import (
    create_test_stock,
    create_test_historical_prices,
    create_test_fundamentals,
    create_test_shareholding_pattern
)

@pytest.mark.asyncio
async def test_stock_search(client: AsyncClient, db: AsyncSession):
    # Create test stock
    stock_data = create_test_stock()
    stock = Stock(**stock_data)
    db.add(stock)
    await db.commit()

    response = await client.get("/api/v1/stocks/search?text=Test")
    assert response.status_code == 200
    data = response.json()
    assert data["total"] >= 1
    assert len(data["items"]) >= 1
    assert data["items"][0]["name"] == "Test Stock Company"

@pytest.mark.asyncio
async def test_stock_historical_prices(client: AsyncClient, db: AsyncSession):
    # Create test stock and historical prices
    stock_data = create_test_stock()
    stock = Stock(**stock_data)
    db.add(stock)
    await db.commit()

    hist_prices = create_test_historical_prices(stock.wstockcode)
    for price in hist_prices:
        nse_price = StockNSEHistPriceData(**price)
        bse_price = StockBSEHistPriceData(**price)
        db.add(nse_price)
        db.add(bse_price)
    await db.commit()

    response = await client.get(
        f"/api/v1/stocks/wpc/{stock.wpc}/historical",
        params={
            "exchange": "nse",
            "start_date": "2024-01-01",
            "end_date": "2024-03-15"
        }
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "price_date" in data[0]
    assert "open" in data[0]
    assert "close" in data[0]

@pytest.mark.asyncio
async def test_stock_fundamentals(client: AsyncClient, db: AsyncSession):
    # Create test stock
    stock_data = create_test_stock()
    stock = Stock(**stock_data)
    db.add(stock)
    await db.commit()

    response = await client.get(
        f"/api/v1/stocks/wpc/{stock.wpc}/fundamentals",
        params={"exchange": "nse"}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "pe" in data
    assert "pb" in data
    assert "current_ratio" in data

@pytest.mark.asyncio
async def test_stock_technical_indicators(client: AsyncClient, db: AsyncSession):
    # Create test stock
    stock_data = create_test_stock()
    stock = Stock(**stock_data)
    db.add(stock)
    await db.commit()

    response = await client.get(f"/api/v1/stocks/wpc/{stock.wpc}/technical-indicators")
    
    assert response.status_code == 200
    data = response.json()
    assert "rsi" in data
    assert "macd" in data
    assert "ema" in data
    assert "sma" in data
    assert "std" in data

@pytest.mark.asyncio
async def test_stock_returns(client: AsyncClient, db: AsyncSession):
    # Create test stock
    stock_data = create_test_stock()
    stock = Stock(**stock_data)
    db.add(stock)
    await db.commit()

    response = await client.get(f"/api/v1/stocks/wpc/{stock.wpc}/returns")
    
    assert response.status_code == 200
    data = response.json()
    assert "one_month" in data
    assert "three_months" in data
    assert "one_year" in data
    assert "five_years" in data