import stat

from pathlib import Path
from typing import Set

from .config import Config
from .reporter import Report, Reporter


class Generator:

    def __init__(
            self,
            *,
            reporter: Reporter,
            config: Config
    ):
        self.reporter = reporter
        self.config = config

    def _generate(self, reports: Set[Report], folder: Path):
        if not reports:
            return

        generator = MovescuBashGenerator(
            reports=reports,
            script=(folder / 'script.sh'),
            config=self.config
        )
        generator.generate()

    def generate(self):
        self._generate(self.reporter.positive_set, self.config.positive_folder)
        self._generate(self.reporter.negative_set, self.config.negative_folder)
        self._generate(self.reporter.unknown_set, self.config.unknown_folder)


class MovescuBashGenerator:

    HEADER: str = '#!/bin/bash\n\n'
    TEMPLATE: str = 'movescu -v -S -k 0008,0052="STUDY" ' \
                    '-k 0020,000D="{suid}" ' \
                    '-aem {aem} -aet {aet} -aec {aec} ' \
                    '{ip} {port}\n'

    def __init__(
            self,
            *,
            reports: Set[Report],
            script: Path,
            config: Config
    ):
        self.reports = reports
        self.script = script
        self.config = config

    def _make_command(self, suid: str) -> str:
        return self.TEMPLATE.format(suid=suid, **self.config.__dict__)

    def generate(self):
        with self.script.open('w') as f:
            f.write(self.HEADER)

            for report in self.reports:
                command = self._make_command(report.suid)
                f.write(command)

        self.script.chmod(self.script.stat().st_mode | stat.S_IEXEC)
