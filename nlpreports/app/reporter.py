from typing import Set, Union

from .constants import ReportType
from .processors import Processor
from .readers import Reader


class Report:

    def __init__(
            self,
            *,
            reader: Reader,
            processor: Processor
    ):
        self.reader = reader
        self.processor = processor

    @property
    def type(
            self
    ) -> Union[ReportType.POSITIVE.value,
               ReportType.NEGATIVE.value,
               ReportType.UNKNOWN.value]:
        return self.processor.report_type

    @property
    def suid(self) -> str:
        return self.processor.suid

    def __hash__(self):
        return hash(self.suid)


class Reporter:

    def __init__(self):
        self.positive_set: Set[Report] = set()
        self.negative_set: Set[Report] = set()
        self.unknown_set: Set[Report] = set()

    def _add_to_set(self, report: Report):
        {
            ReportType.POSITIVE.value: self.positive_set,
            ReportType.NEGATIVE.value: self.negative_set,
        }.get(report.type, self.unknown_set).add(report)

    def add(self, processor, reader):
        report: Report = Report(
            reader=reader,
            processor=processor
        )

        self._add_to_set(report)
