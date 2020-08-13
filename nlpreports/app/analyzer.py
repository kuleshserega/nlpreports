from pathlib import Path

from .config import Config
from .exceptions import Skip
from .generators import Generator
from .getters import FolderGetter, Getter
from .movers import FileMover, Mover
from .processors import Processor, TextProcessor
from .readers import FileReader, Reader
from .reporter import Reporter


class Analyzer:

    def __init__(
            self,
            *,
            config: Config
    ):
        config.validate()
        self.config: Config = config

        self.reporter: Reporter = self.init_reporter()
        self.getter: Getter = self.init_getter()

    @staticmethod
    def init_reporter() -> Reporter:
        return Reporter()

    def init_getter(self) -> Getter:
        return FolderGetter(
            folder=self.config.folder,
            extension=self.config.report_extension
        )

    @staticmethod
    def init_reader(report: Path) -> Reader:
        return FileReader(report=report)

    def init_processor(self, reader: Reader) -> Processor:
        return TextProcessor(
            report_text=reader.read(),
            exam_keyword=self.config.exam_keyword,
            description_keyword=self.config.description_keyword
        )

    def init_mover(self) -> Mover:
        return FileMover(
            reporter=self.reporter,
            positive_folder=self.config.positive_folder,
            negative_folder=self.config.negative_folder,
            unknown_folder=self.config.unknown_folder,
            is_copy=self.config.is_copy
        )

    def init_generator(self) -> Generator:
        return Generator(
            reporter=self.reporter,
            config=self.config
        )

    def analyze(self):
        for report in self.getter:
            reader = self.init_reader(report=report)
            processor = self.init_processor(reader=reader)

            try:
                processor.process()
            except Skip as skip:
                print(skip, reader)
                continue

            self.reporter.add(processor, reader)

        mover = self.init_mover()
        mover.move()

        generator = self.init_generator()
        generator.generate()
