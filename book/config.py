from pathlib import Path

from jinja2_fragments.fastapi import Jinja2Blocks
from pydantic_settings import BaseSettings

APP_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    APP_DIR: Path = APP_DIR

    STATIC_DIR: Path = APP_DIR / "static"
    TEMPLATE_DIR: Path = APP_DIR / "templates"

    SYMBOL: str = "BTC/USDT"


settings = Settings()  # type: ignore
templates = Jinja2Blocks(directory=settings.TEMPLATE_DIR)
