from __future__ import annotations

from datetime import datetime
from sqlite3 import Connection

from app.core.security import crypto_manager
from app.models.entities import FTPConfig


class FTPConfigService:
    def create_config(self, db: Connection, *, host: str, port: int, username: str, password: str, root_path: str, provider_label: str, user_id: int) -> FTPConfig:
        now = datetime.utcnow().isoformat()
        encrypted_password = crypto_manager.encrypt(password)
        cur = db.execute(
            'INSERT INTO ftp_configs (host, port, username, password_encrypted, root_path, provider_label, created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (host, port, username, encrypted_password, root_path, provider_label, now, now),
        )
        db.execute('INSERT INTO user_ftp_links (user_id, ftp_config_id) VALUES (?, ?)', (user_id, cur.lastrowid))
        return FTPConfig(cur.lastrowid, host, port, username, encrypted_password, root_path, provider_label, now, now)

    def list_for_user(self, db: Connection, user_id: int) -> list[FTPConfig]:
        rows = db.execute(
            'SELECT f.* FROM ftp_configs f JOIN user_ftp_links u ON u.ftp_config_id = f.id WHERE u.user_id = ?',
            (user_id,),
        ).fetchall()
        return [FTPConfig(row['id'], row['host'], row['port'], row['username'], row['password_encrypted'], row['root_path'], row['provider_label'], row['created_at'], row['updated_at']) for row in rows]

    def get_decrypted_password(self, config: FTPConfig) -> str:
        return crypto_manager.decrypt(config.password_encrypted)
