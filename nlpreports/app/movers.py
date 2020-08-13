from abc import ABC, abstractmethod
from pathlib import Path
from shutil import copy, move
from typing import Set, Union

from .reporter import Report, Reporter


class Mover(ABC):

    @abstractmethod
    def move(self):
        pass


class FileMover(Mover):

    def __init__(
            self,
            *,
            reporter: Reporter,
            positive_folder: Path,
            negative_folder: Path,
            unknown_folder: Path,
            is_copy: bool
    ):
        self.reporter = reporter
        self.positive_folder = positive_folder
        self.negative_folder = negative_folder
        self.unknown_folder = unknown_folder
        self.is_copy = is_copy

        self.make_directories()

    def make_directories(self):
        if not self.positive_folder.exists():
            self.positive_folder.mkdir()
        if not self.negative_folder.exists():
            self.negative_folder.mkdir()
        if not self.unknown_folder.exists():
            self.unknown_folder.mkdir()

    @property
    def func(self) -> Union[copy, move]:
        return self.is_copy and copy or move

    def _move(self, reports: Set[Report], folder: Path):
        for report in reports:
            src = report.reader.report.absolute()
            dst = (folder / report.reader.report.name).absolute()

            self.func(src, dst)

    def move(self):
        self._move(self.reporter.positive_set, self.positive_folder)
        self._move(self.reporter.negative_set, self.negative_folder)
        self._move(self.reporter.unknown_set, self.unknown_folder)
