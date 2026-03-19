from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class User:
    id: int
    username: str
    password_hash: str
    status: str
    is_admin: bool
    is_active: bool
    created_at: str
    last_login: str | None = None


@dataclass(slots=True)
class FTPConfig:
    id: int
    host: str
    port: int
    username: str
    password_encrypted: str
    root_path: str
    provider_label: str
    created_at: str
    updated_at: str


@dataclass(slots=True)
class LiveStatus:
    id: int
    user_id: int
    ftp_id: int
    status: str
    last_update: str


@dataclass(slots=True)
class AuditLog:
    id: int
    user_id: int | None
    action: str
    target_path: str | None
    timestamp: str
    status: str
    ip_address: str | None
    details: str | None
