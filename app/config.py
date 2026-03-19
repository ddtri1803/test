from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from pathlib import Path


def _default_key() -> str:
    return base64.urlsafe_b64encode(os.urandom(32)).decode("utf-8")


@dataclass(slots=True)
class Settings:
    database_url: str = os.getenv("FTP_MANAGER_DB_URL", f"sqlite:///{Path('ftp_manager.db').resolve()}")
    jwt_secret: str = os.getenv("FTP_MANAGER_JWT_SECRET", "change-me-in-production")
    encryption_key: str = os.getenv("FTP_MANAGER_ENCRYPTION_KEY", _default_key())
    app_name: str = "Secure FTP Manager"
    jwt_expiration_seconds: int = 3600
    rate_limit_attempts: int = 5
    rate_limit_window_seconds: int = 300


settings = Settings()
