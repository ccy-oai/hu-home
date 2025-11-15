"""Settings configuration for Hu's Home."""
from __future__ import annotations

import os
import pathlib
from typing import Any

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
DEFAULT_DB_PATH = BASE_DIR / "hu_home.db"

ENV = os.getenv("FLASK_ENV", default="production")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY", "octocat")
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", f"sqlite:///{DEFAULT_DB_PATH}")
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Websocket / presence tuning
PRESENCE_STALE_AFTER_SECONDS = int(os.getenv("PRESENCE_STALE_AFTER_SECONDS", "90"))


def as_dict() -> dict[str, Any]:  # pragma: no cover - used for debugging
    return {
        "env": ENV,
        "database": SQLALCHEMY_DATABASE_URI,
        "debug": DEBUG,
        "presence_threshold": PRESENCE_STALE_AFTER_SECONDS,
    }
