from abc import ABC, abstractmethod
from pathlib import Path


class Reader(ABC):

    @abstractmethod
    def read(self) -> str:
        pass


class FileReader(Reader):

    def __init__(
            self,
            *,
            report: Path,
    ):
        self.report: Path = report

    @staticmethod
    def _decode(text: bytes) -> str:
        return text.decode('utf-8', 'ignore')

    def read(self) -> str:
        with self.report.open('rb') as f:
            text = f.read()

        return self._decode(text)
