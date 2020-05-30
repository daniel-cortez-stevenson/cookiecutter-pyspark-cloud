"""Common logging facility"""
import logging

import daiquiri
from pythonjsonlogger import jsonlogger


fmt = '%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s %(name)s: %(message)s%(color_stop)s'
json_fmt = '(asctime) (process) (levelname) (name) (message)'

daiquiri.setup(level=logging.INFO, outputs=(
    daiquiri.output.Stream(
        formatter=daiquiri.formatter.ColorFormatter(fmt),
    ),
    daiquiri.output.TimedRotatingFile(
        filename='{{ cookiecutter.package_name }}.log',
        formatter=jsonlogger.JsonFormatter(json_fmt, json_default=str),
    ),
))


def client_logger():
    return daiquiri.getLogger(__name__)
