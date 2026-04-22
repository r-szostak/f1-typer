from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    PROJECT_NAME: str = "F1 Typer API"
    VERSION: str = "1.0.0"
    database_url_async: str
    database_url_sync: str
    redis_url: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    access_token_expire_minutes: int = 10080
    environment: str = "development"

settings = Settings()