import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./oracle.db")
    ASTRO_API_KEY: str = os.getenv("ASTRO_API_KEY", "")
    ASTRO_API_URL: str = os.getenv("ASTRO_API_URL", "https://api.vedicastroapi.com/v3-json")
    
    class Config:
        env_file = ".env"

settings = Settings()