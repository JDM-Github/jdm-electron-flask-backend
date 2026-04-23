import os
import sys
from dotenv import load_dotenv


def _load_env():
    """Load .env from PyInstaller bundle first, then CWD."""
    meipass = getattr(sys, "_MEIPASS", None)
    if meipass:
        load_dotenv(os.path.join(meipass, ".env"))
    load_dotenv(os.path.join(os.path.abspath("."), ".env"), override=False)


_load_env()

class Config:
    """Base configuration. Add your shared env vars here."""
    SECRET_KEY      = os.getenv("SECRET_KEY", "change-me-in-production")
    MAX_WORKERS     = int(os.getenv("MAX_WORKERS", "2"))
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "60"))

    # Example: external API config
    # EXTERNAL_API_URL = os.getenv("EXTERNAL_API_URL", "http://localhost:8000")
    # EXTERNAL_API_KEY = os.getenv("EXTERNAL_API_KEY", "")


class DevelopmentConfig(Config):
    FLASK_ENV = "development"
    DEBUG     = True


class ProductionConfig(Config):
    FLASK_ENV = "production"
    DEBUG     = False
