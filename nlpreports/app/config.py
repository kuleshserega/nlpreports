from ipaddress import ip_address
from pathlib import Path
from typing import Optional

from environ import Env, ImproperlyConfigured


env = Env()
Env.read_env('config.env')


def cast_path(value):
    if not value:
        return None
    return Path(value)


def cast_int_or_none(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None


class Config:

    # Folder where reports
    folder: Path = env('FOLDER', cast=cast_path, default=None)
    # Output folder for positive and negative
    output_folder: Path = env('OUTPUT_FOLDER', cast=cast_path, default=None)

    # Folders name
    positive_bucket_name: str = \
        env('POSITIVE_BUCKET_NAME', cast=str, default='Yes')
    negative_bucket_name: str \
        = env('NEGATIVE_BUCKET_NAME', cast=str, default='No')
    unknown_bucket_name: str = \
        env('UNKNOWN_BUCKET_NAME', cast=str, default='Unknown')

    # Device for movescu
    ip: str = env('IP', cast=str, default=None)
    port: int = env('PORT', cast=cast_int_or_none, default=None)
    aet: str = env('AET', cast=str, default=None)
    aem: str = env('AEM', cast=str, default=None)
    aec: str = env('AEC', cast=str, default=None)

    # File operation copy/move
    is_copy: bool = env('IS_COPY', cast=bool, default=False)

    # Keywords
    exam_keyword: str = env('EXAM_KEYWORD', cast=str, default=None)
    description_keyword: str = \
        env('DESCRIPTION_KEYWORD', cast=str, default=None)

    report_extension: str = env('REPORT_EXTENSION', cast=str, default='txt')

    positive_folder = None
    negative_folder = None
    unknown_folder = None

    def __init__(
            self,
            *,
            folder: Optional[Path] = folder,
            output_folder: Optional[Path] = output_folder,
            positive_bucket_name: Optional[str] = positive_bucket_name,
            negative_bucket_name: Optional[str] = negative_bucket_name,
            unknown_bucket_name: Optional[str] = unknown_bucket_name,
            ip: Optional[str] = ip,
            port: Optional[int] = port,
            aet: Optional[str] = aet,
            aem: Optional[str] = aem,
            aec: Optional[str] = aec,
            is_copy: Optional[bool] = is_copy,
            exam_keyword: Optional[str] = exam_keyword,
            description_keyword: Optional[str] = description_keyword,
            report_extension: Optional[str] = report_extension,
    ):
        self.folder = folder or self.folder
        self.output_folder = output_folder or self.output_folder or self.folder

        self.positive_bucket_name = \
            positive_bucket_name or self.positive_bucket_name
        self.negative_bucket_name = \
            negative_bucket_name or self.negative_bucket_name
        self.unknown_bucket_name = \
            unknown_bucket_name or self.unknown_bucket_name

        self.ip = ip or self.ip
        self.port = port or self.port
        self.aet = aet or self.aet
        self.aem = aem or self.aem
        self.aec = aec or self.aec

        self.is_copy = is_copy or self.is_copy

        self.exam_keyword = exam_keyword or self.exam_keyword
        self.description_keyword = \
            description_keyword or self.description_keyword

        self.report_extension = report_extension or self.report_extension

    def _configure_folders(self):
        self.positive_folder = self.output_folder / self.positive_bucket_name
        self.negative_folder = self.output_folder / self.negative_bucket_name
        self.unknown_folder = self.output_folder / self.unknown_bucket_name

    @staticmethod
    def error(msg):
        raise ImproperlyConfigured(msg)

    def _validate_folder(self):
        if not self.folder:
            self.error('Important FOLDER variable.')

        if not self.folder.exists() or \
                not self.folder.is_dir():
            self.error(f'Directory {self.folder.absolute()} was not found.')

    def _validate_output_folder(self):
        if not self.output_folder.exists() or \
                not self.output_folder.is_dir():
            self.error(f'Directory {self.output_folder.absolute()} '
                       f'was not found.')

    def _validate_ip(self):
        if not self.ip:
            self.error('Important IP variable.')

        try:
            ip_address(self.ip)
        except ValueError:
            self.error('IP address was wrong.')

    def _validate_port(self):
        if not self.port:
            self.error('Important PORT variable.')

        if self.port < 0 or self.port >= 65536:
            self.error('Invalid port number.')

    def _validate_exam_keyword(self):
        if not self.exam_keyword:
            self.error('Important EXAM_KEYWORD variable.')
        self.exam_keyword = self.exam_keyword.lower()

    def _validate_description_keyword(self):
        if not self.description_keyword:
            self.error('Important DESCRIPTION_KEYWORD variable.')
        self.description_keyword = self.description_keyword.lower()

    def validate(self):
        self._validate_folder()
        self._validate_output_folder()

        if not self.positive_bucket_name:
            self.error('Important POSITIVE_BUCKET_NAME variable.')

        if not self.negative_bucket_name:
            self.error('Important NEGATIVE_BUCKET_NAME variable.')

        if not self.unknown_bucket_name:
            self.error('Important UNKNOWN_BUCKET_NAME variable.')

        self._configure_folders()

        self._validate_ip()
        self._validate_port()

        if not self.aet:
            self.error('Important AET variable.')

        if not self.aem:
            self.error('Important AEM variable.')

        if not self.aec:
            self.error('Important AEC variable.')

        self._validate_exam_keyword()
        self._validate_description_keyword()

        if not self.report_extension:
            self.error('Important REPORT_EXTENSION variable.')


def make_config():
    config_template = """POSITIVE_BUCKET_NAME=Yes
NEGATIVE_BUCKET_NAME=No
UNKNOWN_BUCKET_NAME=Unknown
IP=
PORT=
AEM=
AEC=
AET=
IS_COPY=False
EXAM_KEYWORD=
DESCRIPTION_KEYWORD=
FOLDER=
OUTPUT_FOLDER=
REPORT_EXTENSION=txt
"""
    env_file = Path('.') / 'config.env'
    with env_file.open('w') as f:
        f.write(config_template)

    print(f'Config was created at {env_file.absolute()}')
