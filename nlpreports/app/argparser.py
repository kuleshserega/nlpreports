from argparse import Action, ArgumentParser
from pathlib import Path

from .config import Config


class DirectoryAction(Action):

    def __call__(self, parser, namespace, values, option_string=None):
        path = Path(values)

        if not path.exists() or \
                not path.is_dir():
            parser.error(f'Directory `{path.absolute()}` was not found.')

        setattr(namespace, self.dest, path)


params_parser: ArgumentParser = ArgumentParser(
    description='NLP Reports Analyzer'
)

params_parser.add_argument(
    '-f', '--folder',
    action=DirectoryAction,
    dest='folder',
    type=str,
    required=False,
    help='Folder which need to analyze (Incoming). '
         f'(default: {Config.folder.absolute() if Config.folder else None})',
)

params_parser.add_argument(
    '-o', '--output',
    action=DirectoryAction,
    dest='output_folder',
    type=str,
    required=False,
    help='Folder where need to create and use the positive and '
         'the negative folders. '
         '(By default create those folders in the input folder)',
)

params_parser.add_argument(
    '-c',
    action='store_true',
    dest='is_copy',
    default=False,
    required=False,
    help='Just copy the reports, not move. (default: move)'
)

params_parser.add_argument(
    '--ip',
    type=str,
    dest='ip',
    default=Config.ip,
    required=False,
    help=f'IP address for movescu util. (default: {Config.ip!r})',
)

params_parser.add_argument(
    '--port',
    type=int,
    dest='port',
    default=Config.port,
    required=False,
    help=f'Port for movescu util. (default: {Config.port!r})',
)

params_parser.add_argument(
    '--aet',
    type=str,
    dest='aet',
    default=Config.aet,
    required=False,
    help=f'Set my calling AE title. (default: {Config.aet!r})',
)

params_parser.add_argument(
    '--aec',
    type=str,
    dest='aec',
    default=Config.aet,
    required=False,
    help=f'Set called AE title of peer. (default: {Config.aec!r})',
)

params_parser.add_argument(
    '--aem',
    type=str,
    dest='aem',
    default=Config.aet,
    required=False,
    help=f'Set move destination AE title. (default: {Config.aem!r})',
)

params_parser.add_argument(
    '-e', '--exam-keyword',
    type=str,
    dest='exam_keyword',
    default=Config.exam_keyword,
    required=False,
    help='Keyword which must be in EXAM section. '
         f'(default: {Config.exam_keyword!r})',
)

params_parser.add_argument(
    '-d', '--description-keyword',
    type=str,
    dest='description_keyword',
    default=Config.description_keyword,
    required=False,
    help='Keyword which must be in DESCRIPTION section. '
         f'(default: {Config.description_keyword!r})'
)

params_parser.add_argument(
    '--makeconfig',
    action='store_true',
    default=False,
    dest='makeconfig',
    help='Make config file in current directory.',
)
