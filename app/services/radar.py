"""Utilities for interacting with the Radar API."""
from typing import Optional

from radar import RadarClient

from app import settings


def _create_client() -> Optional[RadarClient]:
    secret_key = settings.RADAR_SECRET_KEY
    if not secret_key:
        return None
    return RadarClient(secret_key)


radar_client = _create_client()


def radar_enabled() -> bool:
    """Return True when a Radar client can be used."""
    return radar_client is not None
