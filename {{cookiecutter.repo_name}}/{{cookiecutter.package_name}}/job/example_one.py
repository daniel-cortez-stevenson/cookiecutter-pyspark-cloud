"""
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
from {{cookiecutter.package_name}}.common.util import list_s3_keys
from {{cookiecutter.package_name}}.logger import logger


logger = logger()


def main(spark, bucket, prefix, suffix, **kwargs):
    """Example One Job of PySpark on AWS EMR."""
    keys = list_s3_keys(bucket=bucket, prefix=prefix, suffix=suffix)
    logger.info(f'Found keys! -> {keys}')
