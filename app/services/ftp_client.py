from __future__ import annotations

from dataclasses import dataclass
from ftplib import FTP, FTP_TLS, error_perm
from io import BytesIO

from app.models.entities import FTPConfig
from app.services.ftp_config_service import FTPConfigService


@dataclass(slots=True)
class FTPEntry:
    name: str
    is_dir: bool
    size: int | None = None


class FTPGateway:
    def __init__(self, config_service: FTPConfigService | None = None) -> None:
        self._config_service = config_service or FTPConfigService()
        self._client: FTP | FTP_TLS | None = None

    def connect(self, config: FTPConfig, *, use_tls: bool = True) -> FTP | FTP_TLS:
        password = self._config_service.get_decrypted_password(config)
        client: FTP | FTP_TLS = FTP_TLS() if use_tls else FTP()
        client.connect(config.host, config.port, timeout=15)
        client.login(config.username, password)
        if use_tls and isinstance(client, FTP_TLS):
            client.prot_p()
        client.cwd(config.root_path)
        self._client = client
        return client

    def list_dir(self, path: str = ".") -> list[FTPEntry]:
        if self._client is None:
            raise RuntimeError("FTP client not connected")
        entries: list[FTPEntry] = []
        for line in self._client.mlsd(path):
            name, facts = line
            entries.append(FTPEntry(name=name, is_dir=facts.get("type") == "dir", size=int(facts["size"]) if "size" in facts else None))
        return entries

    def upload_bytes(self, remote_name: str, payload: bytes) -> None:
        if self._client is None:
            raise RuntimeError("FTP client not connected")
        self._client.storbinary(f"STOR {remote_name}", BytesIO(payload))

    def delete(self, remote_path: str) -> None:
        if self._client is None:
            raise RuntimeError("FTP client not connected")
        try:
            self._client.delete(remote_path)
        except error_perm:
            self._client.rmd(remote_path)

    def rename(self, old: str, new: str) -> None:
        if self._client is None:
            raise RuntimeError("FTP client not connected")
        self._client.rename(old, new)

    def disconnect(self) -> None:
        if self._client is not None:
            try:
                self._client.quit()
            finally:
                self._client = None
