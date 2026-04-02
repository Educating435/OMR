from pathlib import Path
from typing import Protocol


class StorageService(Protocol):
    def resolve(self, relative_path: str | Path) -> Path:
        ...

