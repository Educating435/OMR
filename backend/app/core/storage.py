from pathlib import Path

from app.core.config import settings


class StorageManager:
    def __init__(self, root: str | None = None) -> None:
        self.root = Path(root or settings.storage_root)
        self.root.mkdir(parents=True, exist_ok=True)

    def resolve(self, relative_path: str | Path) -> Path:
        path = self.root / Path(relative_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path

