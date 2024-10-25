from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Index, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField
from app.core.config import settings
from enum import Enum as PyEnum

class ScreenerSource(PyEnum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class ScreenerIDGenerator(Base):
    __tablename__ = "screener_id_generator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)

class Screener(Base):
    __tablename__ = "screeners"

    wpc = Column(WealthyProductCodeField(prefix="SCR", Modal=ScreenerIDGenerator, max_length=13), primary_key=True)
    name = Column(String(254), nullable=False)
    source = Column(Enum(ScreenerSource), default=ScreenerSource.Wealthy)
    category = Column(String(254), nullable=False)
    category_display_name = Column(String(254), nullable=False)
    instrument_type = Column(String(254), nullable=False)
    description = Column(String, nullable=True)
    refresh_rate = Column(Integer, default=24 * 60 * 60)
    additional_data = Column(JSON, default=list)
    query_params = Column(JSON, default=dict)
    uri = Column(String, nullable=False)
    is_active = Column(Boolean, default=False)
    order = Column(Integer, default=1)
    category_order = Column(Integer, default=1)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    instruments = relationship("ScreenerInstrument", back_populates="screener")

    __table_args__ = (
        Index('ix_screener_category', 'category'),
        Index('ix_screener_instrument_type', 'instrument_type'),
    )

class ScreenerInstrument(Base):
    __tablename__ = "screener_instruments"

    id = Column(Integer, primary_key=True, index=True)
    screener_wpc = Column(String(13), ForeignKey("screeners.wpc"), nullable=False)
    instruments = Column(JSON, nullable=False)
    cols = Column(JSON, default=list)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    screener = relationship("Screener", back_populates="instruments")

    __table_args__ = (
        Index('ix_screener_instrument_screener_wpc', 'screener_wpc'),
    )



class ISINWPCMapping(Base):
    __tablename__ = "isin_wpc_mapping"

    external_id = Column(WealthyExternalIdField(prefix="isin_wpc_map_"), primary_key=True)
    isin = Column(String(20), nullable=False)
    wpc = Column(String(12), nullable=False)
    hidden = Column(Boolean, default=False)

    __table_args__ = (
        Index('ix_iwm_isin', 'isin'),
        Index('ix_iwm_wpc', 'wpc'),
    )
