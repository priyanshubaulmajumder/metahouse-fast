from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Screener API"
    SQLALCHEMY_DATABASE_URI: str = "postgresql+psycopg2://postgres:root@localhost:5432/postgres"

    class Config:
        env_file = ".env"

settings = Settings()
