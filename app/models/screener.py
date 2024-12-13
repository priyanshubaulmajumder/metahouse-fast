from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, JSON, Index, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField
from app.core.config import settings
from enum import Enum as PyEnum
from app.models.base import BaseModel
class ScreenerSource(PyEnum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class ScreenerIDGenerator(Base):
    __tablename__ = "funnal_screeneridgenerator"
    generated_id = Column(Integer, primary_key=True, autoincrement=True)

class Screener(BaseModel):
    __tablename__ = "funnal_screener"

    wpc = WealthyProductCodeField(prefix="SCR", Modal=ScreenerIDGenerator, max_length=13, primary_key=True,nullable=True,unique=True)
    name = Column(String(254), nullable=False)
    source = Column(Enum(ScreenerSource), default=ScreenerSource.Wealthy)
    category = Column(String(254), nullable=False,primary_key=True)
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

    __table_args__ = (
        Index('ix_screener_category', 'category'),
        Index('ix_screener_instrument_type', 'instrument_type'),
    )
'''def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.category:
            self.category = str(self.category).strip().lower().replace(' ', '-')
        if self.instrument_type:
            self.instrument_type = str(self.instrument_type).strip().lower().replace(' ', '_')
        # delete respective caches as the data has been updated.
        if self.is_active:
            generic_cache_key = CacheKeysService.screener_cache_key(instrument_type=self.instrument_type)
            if generic_cache_key:
                cache.delete(generic_cache_key)
            cache_key = CacheKeysService.screener_cache_key(category=self.category)
            if cache_key:
                cache.delete(cache_key)
            if self.wpc:
                cache_key = CacheKeysService.specific_screener_cache_key(str(self.wpc))
                if cache_key:
                    cache.delete(cache_key)
        super(Screener, self).save(
            force_insert=force_insert, force_update=force_update, using=using, update_fields=update_fields
        )
'''

class ScreenerInstrument(BaseModel):
    __tablename__ = "funnal_screenerinstrument"  # Corrected table name

    id = Column(Integer, primary_key=True, index=True)
    screener = Column(String(13), nullable=False)
    instruments = Column(JSON, nullable=False)
    cols = Column(JSON, default=list)


#    screener = relationship("Screener", back_populates="instruments")

    __table_args__ = (
        Index('ix_screener_instrument_screener_wpc', 'screener'),
    )


