from __future__ import annotations

import sqlite3
from contextlib import contextmanager

from app.config import settings

SCHEMA_SQL = '''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'active',
    is_admin INTEGER NOT NULL DEFAULT 0,
    is_active INTEGER NOT NULL DEFAULT 1,
    created_at TEXT NOT NULL,
    last_login TEXT
);
CREATE TABLE IF NOT EXISTS ftp_configs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    host TEXT NOT NULL,
    port INTEGER NOT NULL,
    username TEXT NOT NULL,
    password_encrypted TEXT NOT NULL,
    root_path TEXT NOT NULL,
    provider_label TEXT NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS user_ftp_links (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ftp_config_id INTEGER NOT NULL,
    UNIQUE(user_id, ftp_config_id)
);
CREATE TABLE IF NOT EXISTS live_status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    ftp_id INTEGER NOT NULL,
    status TEXT NOT NULL,
    last_update TEXT NOT NULL,
    UNIQUE(user_id, ftp_id)
);
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    action TEXT NOT NULL,
    target_path TEXT,
    timestamp TEXT NOT NULL,
    status TEXT NOT NULL,
    ip_address TEXT,
    details TEXT
);
'''


class Database:
    def __init__(self, url: str | None = None) -> None:
        raw = url or settings.database_url
        self.path = raw.removeprefix('sqlite:///') if raw.startswith('sqlite:///') else raw

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        finally:
            conn.close()

    def init_schema(self) -> None:
        with self.connect() as conn:
            conn.executescript(SCHEMA_SQL)


database = Database()
