from __future__ import annotations

from datetime import datetime
from sqlite3 import Connection

from app.models.entities import LiveStatus
from app.services.audit_service import AuditService


class LiveStatusService:
    def __init__(self) -> None:
        self.audit = AuditService()

    def update(self, db: Connection, *, user_id: int, ftp_id: int, status: str, target_path: str | None = None) -> LiveStatus:
        now = datetime.utcnow().isoformat()
        row = db.execute('SELECT * FROM live_status WHERE user_id = ? AND ftp_id = ?', (user_id, ftp_id)).fetchone()
        if row is None:
            cur = db.execute('INSERT INTO live_status (user_id, ftp_id, status, last_update) VALUES (?, ?, ?, ?)', (user_id, ftp_id, status, now))
            record = LiveStatus(cur.lastrowid, user_id, ftp_id, status, now)
        else:
            db.execute('UPDATE live_status SET status = ?, last_update = ? WHERE id = ?', (status, now, row['id']))
            record = LiveStatus(row['id'], user_id, ftp_id, status, now)
        self.audit.log(db, user_id=user_id, action='live_status_update', status=status, target_path=target_path)
        return record
