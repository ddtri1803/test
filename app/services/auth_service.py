from __future__ import annotations

from datetime import datetime
from sqlite3 import Connection

from app.config import settings
from app.core.rate_limit import RateLimiter
from app.core.security import SecurityError, auth_manager
from app.models.entities import User
from app.services.audit_service import AuditService


class AuthService:
    def __init__(self) -> None:
        self.rate_limiter = RateLimiter(settings.rate_limit_attempts, settings.rate_limit_window_seconds)
        self.audit = AuditService()

    def create_user(self, db: Connection, username: str, password: str, *, is_admin: bool = False) -> User:
        created_at = datetime.utcnow().isoformat()
        cur = db.execute(
            'INSERT INTO users (username, password_hash, status, is_admin, is_active, created_at) VALUES (?, ?, ?, ?, ?, ?)',
            (username, auth_manager.hash_password(password), 'active', int(is_admin), 1, created_at),
        )
        user = User(cur.lastrowid, username, '', 'active', is_admin, True, created_at, None)
        self.audit.log(db, user_id=user.id, action='user_created', status='success')
        return user

    def login(self, db: Connection, username: str, password: str, ip_address: str = 'local') -> tuple[User, str]:
        self.rate_limiter.check(f'login:{username}:{ip_address}')
        row = db.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
        if row is None or not row['is_active'] or not auth_manager.verify_password(password, row['password_hash']):
            self.audit.log(db, user_id=row['id'] if row else None, action='login', status='failure', ip_address=ip_address)
            raise SecurityError('Invalid credentials or disabled account')
        last_login = datetime.utcnow().isoformat()
        db.execute('UPDATE users SET last_login = ? WHERE id = ?', (last_login, row['id']))
        token = auth_manager.issue_token(username).token
        self.audit.log(db, user_id=row['id'], action='login', status='success', ip_address=ip_address)
        user = User(row['id'], row['username'], row['password_hash'], row['status'], bool(row['is_admin']), bool(row['is_active']), row['created_at'], last_login)
        return user, token
