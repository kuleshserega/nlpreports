from enum import Enum


class ReportType(Enum):
    POSITIVE: str = 'positive'
    NEGATIVE: str = 'negative'
    UNKNOWN: str = 'unknown'
