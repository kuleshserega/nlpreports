import sys

from .app.analyzer import Analyzer
from .app.argparser import params_parser
from .app.config import Config, make_config


def main():
    params = params_parser.parse_args().__dict__

    makeconfig = params.pop('makeconfig', None)
    if makeconfig:
        make_config()
        sys.exit(0)

    analyzer = Analyzer(config=Config(**params))
    analyzer.analyze()


if __name__ == '__main__':
    main()
