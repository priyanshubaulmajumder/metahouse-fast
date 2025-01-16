# FILE: futils.py
from app.core.config import settings

def is_env_prod() -> bool:
    return settings.ENV.lower() in ["prod", "production"]

def get_float(value, decimal_places=4, default_value=None):
    if value is None:
        return default_value
    try:
        return float(format(float(value), f".{decimal_places}f"))
    except:
        return default_value
    
from typing import List, Optional

async def get_selected_columns(model, cols: Optional[List[str]] = None, exclude_cols: Optional[List[str]] = None):
    """
    Asynchronous helper function to retrieve selected columns excluding specified ones.
    
    Note:
        Since this function performs synchronous operations, making it asynchronous
        does not provide performance benefits. It is recommended to keep it synchronous
        unless you plan to incorporate asynchronous operations in the future.
    """
    if exclude_cols is None:
        exclude_cols = []
    if cols:
        selected = []
        for col in cols:
            if col not in exclude_cols:
                try:
                    selected.append(getattr(model, col))
                except AttributeError:
                    raise ValueError(f"Invalid column specified: {col}")
        if not selected:
            raise ValueError("No valid columns specified for selection after excluding.")
        return selected
    else:
        return [
            getattr(model, column.name)
            for column in model.__table__.columns
            if column.name not in exclude_cols
        ]