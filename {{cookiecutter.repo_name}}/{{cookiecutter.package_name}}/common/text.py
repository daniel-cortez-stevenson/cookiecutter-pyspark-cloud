"""An example of wrapping a Scala UDF with Python code.

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
from pyspark.ml.wrapper import JavaTransformer
from pyspark import keyword_only, since
from pyspark.ml.param.shared import HasInputCol, HasOutputCol
from pyspark.ml.param import Param, Params, TypeConverters
from pyspark.ml.util import JavaMLReadable, JavaMLWritable


class HasLanguage(Params):
    """Mixin for param language"""
    language = Param(Params._dummy(), 'language', 'English or German, etc.', typeConverter=TypeConverters.toString)

    def __init__(self):
        super(HasLanguage, self).__init__()

    def setLanguage(self, value):
        return self._set(language=value)

    def getLanguage(self):
        return self.getOrDefault(self.language)


class SnowballStemmer(JavaTransformer, JavaMLReadable, JavaMLWritable, HasInputCol, HasOutputCol, HasLanguage):
    """Python-wrapped Scala Implementation of the Snowball Stemmer."""

    @keyword_only
    def __init__(self, inputCol=None, outputCol=None, language=None):
        """__init__(inputCol=None, outputCol=None, language=None)"""
        super(SnowballStemmer, self).__init__()
        self._java_obj = self._new_java_obj('org.apache.spark.mllib.feature.Stemmer', self.uid)
        kwargs = self._input_kwargs
        self.setParams(**kwargs)

    @keyword_only
    @since('1.3.0')
    def setParams(self, inputCol=None, outputCol=None, language=None):
        """setParams(inputCol=None, outputCol=None, language=None)"""
        kwargs = self._input_kwargs
        return self._set(**kwargs)
