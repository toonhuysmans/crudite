import os
from pydantic import BaseSettings

class CommonSettings(BaseSettings):
    APP_NAME: str = "Crudite"
    DEBUG_MODE: bool = os.getenv('DEBUG_MODE', False)

class ServerSettings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000

class DatabaseSettings(BaseSettings):
    DB_URL: str = os.getenv('MONGO_URL', "")
    DB_NAME: str = os.getenv('MONGO_DB', "")

class Settings(CommonSettings, ServerSettings, DatabaseSettings):
    pass

settings = Settings()