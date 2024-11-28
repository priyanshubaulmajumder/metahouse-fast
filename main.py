from fastapi import FastAPI
from app.api.v1.router import api_router
from app.core.config import settings
import uvicorn
from app.db.base import validate_database

validate_database()

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=9000, reload=True, log_level="debug")
