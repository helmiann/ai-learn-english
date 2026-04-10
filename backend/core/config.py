# ============================================================
#  ENGLISH GRAMMAR CHATBOT — App Configuration
#  File: backend/core/config.py
# ============================================================

from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ----------------------------------------------------------
    # APLIKASI
    # ----------------------------------------------------------
    APP_NAME: str = "English Grammar Chatbot"
    APP_ENV: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost",
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # ----------------------------------------------------------
    # DATABASE
    # ----------------------------------------------------------
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "grammar_chatbot"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432

    @property
    def DATABASE_URL(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    # ----------------------------------------------------------
    # REDIS
    # ----------------------------------------------------------
    REDIS_URL: str = "redis://localhost:6379/0"
    REDIS_PASSWORD: str = ""

    # ----------------------------------------------------------
    # JWT & KEAMANAN
    # ----------------------------------------------------------
    SECRET_KEY: str = "ganti-dengan-secret-key-yang-kuat"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ----------------------------------------------------------
    # LLAMA API
    # ----------------------------------------------------------
    LLAMA_API_URL: str = ""
    LLAMA_API_KEY: str = ""
    LLAMA_MODEL: str = "llama-3-8b-instruct"
    LLAMA_MAX_TOKENS: int = 2048
    LLAMA_TEMPERATURE: float = 0.7

    # ----------------------------------------------------------
    # LOGGING
    # ----------------------------------------------------------
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"


# Instance tunggal — import ini di file lain
settings = Settings()