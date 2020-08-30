"""Entrypoint for spark-submit. Loaded by EMR from S3 on step execution.

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
import argparse
import datetime
import importlib
import logging
import os

# fmt: off
from {{cookiecutter.package_name}}.common.logging import pyspark_logger
# fmt: on


def main():
    logger = logging.getLogger(__name__)

    logger.debug("looking for the SparkSession ...")
    try:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        logger.info(f"Found SparkSession: {spark}")
    except ImportError:
        msg = "Install pyspark to your Python environment to test locally."
        logger.error(msg)
        raise

    parser = argparse.ArgumentParser(description="Run a PySpark job via spark-submit.")
    parser.add_argument(
        "--job-name",
        type=str,
        required=True,
        dest="job_name",
        help="The name of the job module you want to run. (ex: `--job-name example_one` will run main() in job.example_one module)",
    )
    parser.add_argument(
        "--job-kwargs",
        nargs="*",
        help="Extra keyword-arguments to send to main() of the job module (ex: `--job-kwargs bat=baz foo=bar`",
    )
    args = parser.parse_args()

    logger.info(f"Called {__file__}:main with arguments:", args)

    os.environ.update(
        {"PYSPARK_JOB_ARGS": " ".join(args.job_kwargs) if args.job_kwargs else ""}
    )
    logger.info(f"OS environment:\n{os.environ}")

    job_kwargs = dict()
    if args.job_kwargs:
        for kwarg in args.job_kwargs:
            kw, arg = kwarg.split("=", 1)
            job_kwargs[kw] = arg
    logger.info(f'Submitted job "{args.job_name}" with kwargs: {job_kwargs}')

    try:
        job_module = importlib.import_module(
            f"{{ cookiecutter.package_name }}.job.{args.job_name}"
        )
        logger.info(f"Imported {args.job_name} successfully.")
    except ImportError:
        logger.error("______________ Abrupt Exit ______________")
        logger.error(f"Failed to import {args.job_name}. Exiting.")
        raise

    start = datetime.datetime.now()
    try:
        job_logger = pyspark_logger(spark.sparkContext)
        job_module.main(spark=spark, logger=job_logger, **job_kwargs)
    except Exception:
        logger.error("______________ Abrupt Exit ______________")
        raise
    finally:
        end = datetime.datetime.now()
        duration = end - start
        execution_mins = round(duration.seconds / 60.0, 2)
        logger.info(f"Execution of job {args.job_name} took {execution_mins} minutes.")
    logger.info(f"Finished running {__file__} for job {args.job_name}.")


if __name__ == "__main__":
    main()
