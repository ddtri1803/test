from __future__ import annotations

import tempfile
import unittest

from app.db.session import Database
from app.services.auth_service import AuthService
from app.services.ftp_config_service import FTPConfigService
from app.services.live_status_service import LiveStatusService


class ServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.db = Database(f"{self.tempdir.name}/test.db")
        self.db.init_schema()
        self.auth = AuthService()
        self.ftp = FTPConfigService()
        self.live = LiveStatusService()

    def tearDown(self) -> None:
        self.tempdir.cleanup()

    def test_user_login_and_ftp_config_flow(self) -> None:
        with self.db.connect() as db:
            user = self.auth.create_user(db, 'alice', 'Password123!')
            _, token = self.auth.login(db, 'alice', 'Password123!', ip_address='127.0.0.1')
            self.assertTrue(token)
            config = self.ftp.create_config(
                db,
                host='ftp.example.com',
                port=21,
                username='ftp-user',
                password='ftp-pass',
                root_path='/public_html',
                provider_label='Hostinger',
                user_id=user.id,
            )
            self.assertEqual(self.ftp.get_decrypted_password(config), 'ftp-pass')
            status = self.live.update(db, user_id=user.id, ftp_id=config.id, status='online', target_path='/public_html')
            self.assertEqual(status.status, 'online')
            count = db.execute('SELECT COUNT(*) FROM logs').fetchone()[0]
            stored_user = db.execute('SELECT username FROM users WHERE id = ?', (user.id,)).fetchone()[0]
            stored_live = db.execute('SELECT status FROM live_status WHERE ftp_id = ?', (config.id,)).fetchone()[0]
            self.assertEqual(stored_user, 'alice')
            self.assertEqual(stored_live, 'online')
            self.assertGreaterEqual(count, 3)


if __name__ == '__main__':
    unittest.main()
