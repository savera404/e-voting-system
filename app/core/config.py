from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """
    Design Pattern #1: Singleton Pattern
    ─────────────────────────────────────
    `get_settings()` is decorated with @lru_cache, which means Python will
    construct one Settings instance and reuse it for every subsequent call.
    This guarantees a single source of truth for all configuration values
    throughout the application lifecycle — the classic Singleton guarantee
    without the boilerplate of a __new__ override.
    """

    DATABASE_URL: str
    SECRET_KEY: str 
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24   # 24 hours

    APP_NAME: str = "E-Voting System"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"


@lru_cache()           # ← Singleton: only one Settings object ever created
def get_settings() -> Settings:
    return Settings()


# Module-level convenience alias used everywhere else
settings = get_settings()


#@lru_cache() means: the first time get_settings() is called, Python creates a Settings object and caches it. Every call after that returns the same cached object — it never reads the .env file again.