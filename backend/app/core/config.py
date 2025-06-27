import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./oracle.db")
    
    # Primary Astrology API (AstroAPI.com)
    ASTRO_API_KEY: str = os.getenv("ASTRO_API_KEY", "")
    ASTRO_API_URL: str = os.getenv("ASTRO_API_URL", "https://api.astroapi.com/v1")
    
    # Secondary Astrology API (Prokerala)
    PROKERALA_CLIENT_ID: str = os.getenv("PROKERALA_CLIENT_ID", "")
    PROKERALA_CLIENT_SECRET: str = os.getenv("PROKERALA_CLIENT_SECRET", "")
    PROKERALA_API_URL: str = os.getenv("PROKERALA_API_URL", "https://api.prokerala.com/v2")
    
    # LLM Service (OpenAI)
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    USE_LLM: bool = os.getenv("USE_LLM", "true").lower() == "true"
    
    class Config:
        env_file = ".env"

settings = Settings()