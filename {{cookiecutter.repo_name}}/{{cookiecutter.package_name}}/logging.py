"""Common logging facility"""
import logging

import daiquiri


daiquiri.setup(level=logging.INFO, outputs=(
    daiquiri.output.Stream(),
    daiquiri.output.TimedRotatingFile(
        filename=f'{{ cookiecutter.package_name }}.log',
        formatter=daiquiri.formatter.JSON_FORMATTER,
    ),
))


def client_logger():
    return daiquiri.getLogger(__name__)
