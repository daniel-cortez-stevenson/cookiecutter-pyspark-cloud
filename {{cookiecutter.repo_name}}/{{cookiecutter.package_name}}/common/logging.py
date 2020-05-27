"""Logging utils for when running in a PySpark context"""


def pyspark_logger(spark_context):
    log4jLogger = spark_context._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(__name__)
    logger.info('pyspark logger initialized')
    return logger
