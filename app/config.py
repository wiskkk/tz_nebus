from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    db_url: str = Field(..., alias="DB_URL")
    db_url_sync: str = Field(..., alias="DB_URL_SYNC")
    api_key: str = Field(..., alias="API_KEY")

    class Config:
        extra = "ignore"  # <- вот это ключевое


settings = Settings()
