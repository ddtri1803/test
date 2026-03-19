# Secure FTP Manager

A Python-only FTP management desktop application with:

- PySide6 desktop UI inspired by Finder / VS Code.
- Integrated backend services for app-auth, FTP config management, live status, and audit logging.
- SQLite persistence for users, FTP configs, live status, and logs.
- Encrypted-at-rest FTP credential handling with in-memory decryption during active connections.
- Signed session tokens, nonce/timestamp anti-replay checks, rate limiting, and kill-switch-ready account flags.
- FTP/FTPS browsing service abstraction for any provider exposing standard FTP.

## Run

```bash
python -m app.main
```

## Test

```bash
python -m unittest discover -s tests -v
```
