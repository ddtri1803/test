from __future__ import annotations

from datetime import datetime
from sqlite3 import Connection

from app.models.entities import AuditLog


class AuditService:
    def log(self, db: Connection, *, user_id: int | None, action: str, status: str, target_path: str | None = None, ip_address: str | None = None, details: str | None = None) -> AuditLog:
        timestamp = datetime.utcnow().isoformat()
        cur = db.execute(
            'INSERT INTO logs (user_id, action, target_path, timestamp, status, ip_address, details) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (user_id, action, target_path, timestamp, status, ip_address, details),
        )
        return AuditLog(cur.lastrowid, user_id, action, target_path, timestamp, status, ip_address, details)
