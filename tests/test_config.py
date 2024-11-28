import os
from pathlib import Path

# Get the root directory
ROOT_DIR = Path(__file__).parent.parent

# Test database URL from environment variable or default
TEST_DB_URL = os.getenv(
    "TEST_DB_URL",
    "postgresql+asyncpg://postgres:root@localhost:5432/postgres"
)

# Test settings
TEST_SETTINGS = {
    "TESTING": True,
    "DATABASE_URL": TEST_DB_URL,
    "API_V1_STR": "/api/v1",
    "PROJECT_NAME": "Stock API Test"
} 