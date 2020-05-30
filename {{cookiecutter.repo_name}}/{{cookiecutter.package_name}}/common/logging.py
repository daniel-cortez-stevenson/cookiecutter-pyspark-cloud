"""Logging utils for when running in a PySpark context"""


def pyspark_logger(spark_context, name=__name__):
    log4jLogger = spark_context._jvm.org.apache.log4j
    logger = log4jLogger.LogManager.getLogger(name)
    logger.info('pyspark_logger initialized')
    return logger
