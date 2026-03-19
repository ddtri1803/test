from __future__ import annotations

import unittest
from datetime import datetime, timezone

from app.core.security import SecurityError, auth_manager, crypto_manager


class SecurityTests(unittest.TestCase):
    def test_encrypt_decrypt_roundtrip(self) -> None:
        secret = "ftp-password"
        encrypted = crypto_manager.encrypt(secret)
        self.assertNotEqual(secret, encrypted)
        self.assertEqual(secret, crypto_manager.decrypt(encrypted))

    def test_token_and_replay_validation(self) -> None:
        bundle = auth_manager.issue_token("alice")
        payload = auth_manager.decode_token(bundle.token)
        self.assertEqual(payload["sub"], "alice")
        timestamp = int(datetime.now(timezone.utc).timestamp())
        signature = auth_manager.sign_request(bundle.nonce, timestamp)
        auth_manager.validate_replay_protection(bundle.nonce, timestamp, signature)
        with self.assertRaises(SecurityError):
            auth_manager.validate_replay_protection(bundle.nonce, timestamp, "bad-signature")


if __name__ == "__main__":
    unittest.main()
