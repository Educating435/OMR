from pathlib import Path

from app.core.config import settings


class LocalStorageService:
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or settings.storage_root)

    def resolve(self, relative_path: str | Path) -> Path:
        return self.root / Path(relative_path)

