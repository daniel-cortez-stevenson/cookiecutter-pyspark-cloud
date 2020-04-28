"""Adds functionality to imported classes.

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
from pyspark.sql import DataFrame


def transform(self, f, **kwargs):
    """Transform is widely-used throughout the project to
    'chain' `pyspark.sql.DataFrame` methods using dot-
    notation.

    That being said, this extension could be applied to
    other classes in interesting ways..."""
    return f(self, **kwargs)


DataFrame.transform = transform
DataFrame.transform.__doc__ = """Transform extension applied to `pyspark.sql.DataFrame`"""
