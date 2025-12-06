from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    MONGO_URL: str
    DB_NAME: str = "financetracker"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_HOURS: int = 24 * 30  # 30 days
    OPENAI_API_KEY: Optional[str] = None
    EMERGENT_LLM_KEY: Optional[str] = None

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
