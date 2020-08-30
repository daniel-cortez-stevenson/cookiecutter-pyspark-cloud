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
import pyspark.sql.types as T
from pyspark.ml.feature import RegexTokenizer
from pyspark.ml.pipeline import Pipeline

# fmt: off
from {{cookiecutter.package_name}}.common.text import SnowballStemmer
# fmt: on


def main(spark, logger, **kwargs):
    logger.info("Creating a simple DataFrame ...")
    schema_names = ["id", "german_text"]
    fields = [
        T.StructField(field_name, T.StringType(), True) for field_name in schema_names
    ]
    schema = T.StructType(fields)
    data = [
        ("abc", "Hallo Herr Mustermann"),
        ("xyz", "Deutsch ist das Ding!"),
    ]
    df = spark.createDataFrame(data, schema)
    df.show()

    logger.info("Building the ML pipeline ...")
    tokenizer = RegexTokenizer(
        inputCol="german_text", outputCol="tokens", pattern="\\s+"
    )
    stemmer = SnowballStemmer(
        inputCol="tokens", outputCol="stemmed_tokens", language="German"
    )
    stemming_pipeline = Pipeline(
        stages=[
            tokenizer,
            stemmer,
        ]
    )

    logger.info("Running the stemming ML pipeline ...")
    stemmed_df = stemming_pipeline.fit(df).transform(df)
    stemmed_df.show()
