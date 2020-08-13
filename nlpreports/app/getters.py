from abc import ABC, abstractmethod
from pathlib import Path
from typing import List


class Getter(ABC):

    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class FolderGetter(Getter):

    def __init__(
            self,
            *,
            folder: Path,
            extension: str
    ):
        self.folder: Path = folder
        self.extension: str = extension

        self._files: List[Path] = list(self.folder.glob(f'*.{self.extension}'))
        self._current: int = 0

    def __next__(self) -> Path:
        if not self._files:
            raise StopIteration

        self._current += 1

        try:
            return self._files[self._current - 1]
        except IndexError:
            raise StopIteration
