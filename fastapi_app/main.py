from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from fastapi import FastAPI

class DBSettings(BaseSettings):
    db_name: str
    db_user: str
    db_password: SecretStr
    db_host: str
    db_port: int
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf8", extra="ignore")

    @property
    def db_url(self):
        return f"postgresql+asyncpg://{self.db_user}:{self.db_password.get_secret_value()}@{self.db_host}:{self.db_port}/{self.db_name}"

class Settings(BaseSettings):
    db_settings: DBSettings = DBSettings()

settings = Settings()

app = FastAPI()

@app.get("/db_url")
async def db_url():
    return {"database_url": settings.db_settings.db_url}

@app.get("/")
async def root():
    return {"message": "Hello, FastAPI!"}

