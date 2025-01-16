from sqlmodel import Field, SQLModel, Enum, JSON, Index  # Replace SQLAlchemy imports with SQLModel imports
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from app.utils.model_utils import WealthyProductCodeField, WealthyExternalIdField
from app.core.config import settings
from enum import Enum as PyEnum
from app.models.base import BaseModel
from typing import List,Dict
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy import Column, String, JSON  # Add Column import from sqlalchemy
from sqlalchemy.dialects.postgresql import JSONB
class ScreenerSource(PyEnum):
    Wealthy = 'wealthy'
    CMOTS = 'cmots'
    MorningStar = 'morning_star'

class ScreenerIDGenerator(BaseModel, table=True):
    __tablename__ = "funnal_screeneridgenerator"
    generated_id: int = Field(primary_key=True)
    

class Screener(BaseModel, table=True):
    __tablename__ = "funnal_screener"
    class Config:
        arbitrary_types_allowed = True
        use_enum_values = True
        
    wpc: str = WealthyProductCodeField(prefix="SCR", Modal=ScreenerIDGenerator, max_length=13, primary_key=True, nullable=True, unique=True)
    name: str = Field(max_length=254, nullable=False)
    source: ScreenerSource = Field(default=ScreenerSource.Wealthy)
    category: str = Field(max_length=254, nullable=False, primary_key=True)
    category_display_name: str = Field(max_length=254, nullable=False)
    instrument_type: str = Field(max_length=254, nullable=False)
    description: str = Field(nullable=True)
    refresh_rate: int = Field(default=24 * 60 * 60)
    additional_data: List[str] = Field(sa_column=Column(ARRAY(String)), default_factory=list)  # Use ARRAY for a list of strings
    query_params: Dict[str, str] = Field(sa_column=Column(JSONB), default_factory=dict)  # Use JSONB for a dictionary
    uri: str = Field(nullable=False)
    is_active: bool = Field(default=False)
    order: int = Field(default=1)
    category_order: int = Field(default=1)
    
    __table_args__ = (
        Index('ix_screener_category', 'category'),
        Index('ix_screener_instrument_type', 'instrument_type'),
    )

class ScreenerInstrument(BaseModel, table=True):
    __tablename__ = "funnal_screenerinstrument"  
    class Config:
        arbitrary_types_allowed = True
    id: int = Field(primary_key=True)
    screener: str = Field(max_length=13, nullable=False)
    instruments: dict = Field(sa_column=Column(JSONB))
    cols: list = Field(sa_column=Column(ARRAY(String)), default_factory=list)

    __table_args__ = (
        Index('ix_screener_instrument_screener_wpc', 'screener'),
    )


