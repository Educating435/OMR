from pathlib import Path
from typing import Protocol


class StorageProvider(Protocol):
    def save_bytes(self, relative_path: str, content: bytes) -> str:
        ...

    def absolute_path(self, relative_path: str) -> Path:
        ...
