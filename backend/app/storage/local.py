from pathlib import Path

from app.database.config import settings


class LocalStorageProvider:
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or settings.storage_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def save_bytes(self, relative_path: str, content: bytes) -> str:
        target = self.root / relative_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(content)
        return target.as_posix()

    def absolute_path(self, relative_path: str) -> Path:
        return (self.root / relative_path).resolve()
