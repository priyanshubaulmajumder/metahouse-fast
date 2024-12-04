from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Stock Screener API"
    postgres_database_uri: str = "postgresql+psycopg2://postgres:root@localhost:5432/metahouse"
    ECHO_SQL: bool = True    # Add this line to include the ECHO_SQL setting

    class Config:
        env_file = ".env"

settings = Settings()
