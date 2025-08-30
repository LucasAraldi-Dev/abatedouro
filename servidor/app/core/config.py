from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List
import os

class Settings(BaseSettings):
    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}
    APP_NAME: str = Field(default="Abatedouro API")
    API_V1_STR: str = Field(default="/api/v1")
    MONGODB_URI: str | None = Field(default=None)
    MONGODB_DBNAME: str = Field(default="abatedouro")
    BACKEND_CORS_ORIGINS: str = Field(default="http://localhost:5173,http://127.0.0.1:5173")
    
    @property
    def cors_origins(self) -> List[str]:
        """Convert CORS string to list"""
        if not self.BACKEND_CORS_ORIGINS:
            return []
        return [x.strip() for x in self.BACKEND_CORS_ORIGINS.split(",") if x.strip()]

settings = Settings()