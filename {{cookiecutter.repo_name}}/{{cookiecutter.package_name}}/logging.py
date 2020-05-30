"""Common logging facility

Copyright 2020 Daniel Cortez Stevenson

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    https://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
import logging

import daiquiri
from pythonjsonlogger import jsonlogger


stream_fmt = '%(asctime)s [%(process)d] %(color)s%(levelname)-8.8s %(name)s: %(message)s%(color_stop)s'
json_fmt = '(asctime) (process) (levelname) (name) (message)'

daiquiri.setup(level=logging.INFO, outputs=(
    daiquiri.output.Stream(
        formatter=daiquiri.formatter.ColorFormatter(stream_fmt),
    ),
    daiquiri.output.TimedRotatingFile(
        filename='{{ cookiecutter.package_name }}.log',
        formatter=jsonlogger.JsonFormatter(json_fmt, json_default=str),
    ),
))


def client_logger(name=__name__):
    return daiquiri.getLogger(name)
