"""Application configuration."""
from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    database_url: str = os.getenv("DATABASE_URL", "sqlite:///app.db")
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret")
    env: str = os.getenv("FLASK_ENV", "production")

    @property
    def flask_config(self) -> dict:
        return {
            "SQLALCHEMY_DATABASE_URI": self.database_url,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "SECRET_KEY": self.secret_key,
        }


DEFAULT_SETTINGS = Settings()

