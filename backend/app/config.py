from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    APP_NAME: str = "MasterCS"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True

    # Database — MySQL
    DATABASE_URL: str = "mysql+pymysql://root@localhost/mastercs"

    # JWT
    SECRET_KEY: str = "change-this-to-a-secure-random-key-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440  # 24 hours

    # Learning Engine
    NEW_QUESTION_RATIO: float = 0.50
    WEAK_QUESTION_RATIO: float = 0.30
    REVISION_QUESTION_RATIO: float = 0.20
    QUESTION_COOLDOWN_HOURS: int = 4
    MASTERY_THRESHOLD_LEARNING: float = 0.25
    MASTERY_THRESHOLD_FAMILIAR: float = 0.50
    MASTERY_THRESHOLD_PROFICIENT: float = 0.75
    MASTERY_THRESHOLD_MASTERED: float = 0.90

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
