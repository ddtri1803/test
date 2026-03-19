from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone

from app.config import settings


class SecurityError(Exception):
    pass


@dataclass(slots=True)
class TokenBundle:
    token: str
    expires_at: datetime
    nonce: str


class CryptoManager:
    def __init__(self, key_material: str) -> None:
        self._key = hashlib.sha256(key_material.encode('utf-8')).digest()

    def encrypt(self, plaintext: str) -> str:
        nonce = os.urandom(16)
        payload = plaintext.encode('utf-8')
        cipher = bytes(b ^ self._key[i % len(self._key)] ^ nonce[i % len(nonce)] for i, b in enumerate(payload))
        return base64.b64encode(nonce + cipher).decode('utf-8')

    def decrypt(self, ciphertext: str) -> str:
        raw = base64.b64decode(ciphertext.encode('utf-8'))
        nonce, cipher = raw[:16], raw[16:]
        payload = bytes(b ^ self._key[i % len(self._key)] ^ nonce[i % len(nonce)] for i, b in enumerate(cipher))
        return payload.decode('utf-8')


class AuthManager:
    def __init__(self, secret: str) -> None:
        self._secret = secret.encode('utf-8')

    def hash_password(self, password: str) -> str:
        salt = os.urandom(16)
        digest = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
        return base64.b64encode(salt + digest).decode('utf-8')

    def verify_password(self, password: str, password_hash: str) -> bool:
        raw = base64.b64decode(password_hash.encode('utf-8'))
        salt, digest = raw[:16], raw[16:]
        candidate = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 120000)
        return hmac.compare_digest(candidate, digest)

    def _b64(self, value: bytes) -> str:
        return base64.urlsafe_b64encode(value).rstrip(b'=').decode('utf-8')

    def issue_token(self, subject: str) -> TokenBundle:
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=settings.jwt_expiration_seconds)
        nonce = self._b64(os.urandom(12))
        header = self._b64(json.dumps({'alg': 'HS256', 'typ': 'JWT'}).encode('utf-8'))
        payload = self._b64(json.dumps({'sub': subject, 'iat': int(now.timestamp()), 'exp': int(expires_at.timestamp()), 'nonce': nonce}).encode('utf-8'))
        signature = self._b64(hmac.new(self._secret, f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest())
        return TokenBundle(token=f'{header}.{payload}.{signature}', expires_at=expires_at, nonce=nonce)

    def decode_token(self, token: str) -> dict:
        try:
            header, payload, signature = token.split('.')
        except ValueError as exc:
            raise SecurityError('Malformed token') from exc
        expected = self._b64(hmac.new(self._secret, f'{header}.{payload}'.encode('utf-8'), hashlib.sha256).digest())
        if not hmac.compare_digest(expected, signature):
            raise SecurityError('Invalid token signature')
        padded = payload + '=' * (-len(payload) % 4)
        data = json.loads(base64.urlsafe_b64decode(padded.encode('utf-8')))
        if int(datetime.now(timezone.utc).timestamp()) > data['exp']:
            raise SecurityError('Token expired')
        return data

    def sign_request(self, token_nonce: str, timestamp: int) -> str:
        return hmac.new(self._secret, f'{token_nonce}:{timestamp}'.encode('utf-8'), hashlib.sha256).hexdigest()

    def validate_replay_protection(self, token_nonce: str, timestamp: int, signature: str, window_seconds: int = 60) -> None:
        now = int(datetime.now(timezone.utc).timestamp())
        if abs(now - timestamp) > window_seconds:
            raise SecurityError('Request timestamp outside allowed window')
        expected = self.sign_request(token_nonce, timestamp)
        if not hmac.compare_digest(expected, signature):
            raise SecurityError('Invalid request signature')


crypto_manager = CryptoManager(settings.encryption_key)
auth_manager = AuthManager(settings.jwt_secret)
