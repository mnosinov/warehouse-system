import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+asyncpg://warehouse:warehouse123@localhost/warehouse_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "fjkelkKKKLEKWJ2398409380LJJekjrKUUQTTWQ6123617239")
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))

settings = Settings()