from pathlib import Path

from jinja2_fragments.fastapi import Jinja2Blocks
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import MongoDsn
from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    ENV: str = "production"
    APP_DIR: Path = APP_DIR
    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATE_DIR: Path = APP_DIR / "templates"
    MONGO_DSN: MongoDsn = "mongodb://localhost:27017/?directConnection=true"  # type: ignore
    DB_NAME: str = "book"
    SYMBOL: str = "BTC/USDT"


settings = Settings()  # type: ignore
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)
mongo = AsyncIOMotorClient(str(settings.MONGO_DSN))
