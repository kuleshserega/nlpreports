import re

from abc import ABC, abstractmethod
from typing import Optional, Union

from .constants import ReportType
from .exceptions import Skip


class Processor(ABC):

    @property
    @abstractmethod
    def suid(self) -> str:
        pass

    @property
    @abstractmethod
    def report_type(
            self
    ) -> Union[ReportType.POSITIVE.value,
               ReportType.NEGATIVE.value,
               ReportType.UNKNOWN.value]:
        pass

    @abstractmethod
    def process(self):
        pass


class TextProcessor(Processor):

    SUID_REGEXP = re.compile(r'SUID:[\n\s\t]*([\d.]+)', flags=re.IGNORECASE)
    EXAM_REGEXP = re.compile(r'EXAM:([^:]+)', flags=re.IGNORECASE)

    def __init__(
            self,
            *,
            report_text: str,
            exam_keyword: str,
            description_keyword: str
    ):
        self.report_text: str = report_text
        self.exam_keyword: str = exam_keyword
        self.description_keyword: str = description_keyword

        self.__suid = None
        self.__report_type = None

    @property
    def suid(self) -> str:
        return self.__suid

    @property
    def report_type(
            self
    ) -> Union[ReportType.POSITIVE.value,
               ReportType.NEGATIVE.value,
               ReportType.UNKNOWN.value]:
        return self.__report_type

    def _parse_suid(self, text: str):
        match = self.SUID_REGEXP.search(text)
        if not match:
            raise Skip('Cannot find a SUID')
        self.__suid = match.group(1)

    def _get_exam_section(self, text: str) -> Optional[str]:
        match = self.EXAM_REGEXP.search(text)
        if not match:
            return
        return match.group(1)

    def _check_exam_section(self, exam_section: str) -> bool:
        return self.exam_keyword in exam_section.lower()

    def _get_description_section(self, exam_section: str) -> str:
        return self.report_text.split(exam_section)[-1]

    def _check_description_section(self, description_section: str) -> bool:
        return self.description_keyword in description_section.lower()

    def process(self):
        # Parse SUID
        self._parse_suid(self.report_text)

        # Parse exam section
        exam_section = self._get_exam_section(self.report_text)
        if not exam_section:
            self.__report_type = ReportType.UNKNOWN.value
            return

        # Check exam section
        if not self._check_exam_section(exam_section):
            self.__report_type = ReportType.NEGATIVE.value
            return

        # Check section above exam (description)
        description_section = self._get_description_section(exam_section)
        if not self._check_description_section(description_section):
            self.__report_type = ReportType.NEGATIVE.value
            return

        self.__report_type = ReportType.POSITIVE.value
