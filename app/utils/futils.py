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
    
