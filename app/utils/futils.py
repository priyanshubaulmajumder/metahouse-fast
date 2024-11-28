# FILE: futils.py
from app.core.config import settings

def is_env_prod() -> bool:
    return settings.ENV.lower() in ["prod", "production"]