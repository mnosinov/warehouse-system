import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(
        os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
    )

    # Debug и настройки разработки
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    if DEBUG:
        allow_origins: list[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    else:
        allow_origins = None

    CORS_ORIGINS: list[str] = os.getenv(
        "CORS_ORIGINS", allow_origins or "http://localhost:3000"
    ).split(",")

    # Настройки базы данных для разработки
    DB_ECHO: bool = (
        os.getenv("DB_ECHO", "False").lower() == "true"
    )  # Логировать SQL запросы


settings = Settings()
