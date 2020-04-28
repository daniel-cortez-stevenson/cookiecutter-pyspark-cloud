#!/usr/bin/env bash
#
# Copyright 2020 Daniel Cortez Stevenson
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# Installs EMR-relevant pypackages to EC2 Instances with a python3.6 bin
# - Focus on installing pypackages with external (C) dependencies
# - Other pypackages can be sent at runtime with an Apache Livy (or other) API call
#
# Usage:
#   sh bootstrap-pylibs.sh

set -x -e

# to fix strange path error on stderr - something with Debian
export PATH=/usr/local/bin:$PATH

# Install and update cluster-wide pypackages in our preferred Python (python3.6 bin)
sudo easy_install-3.6 pip
sudo /usr/local/bin/pip3.6 install --upgrade pip
sudo /usr/local/bin/pip3.6 install --upgrade \
  abydos==0.4.0 \
  boto3 \
  cython \
  findspark \
  fuzzywuzzy==0.17.0 \
  h5py \
  hdfs3 \
  jsonschema \
  numpy \
  pandas \
  py4j \
  pyarrow \
  scikit-learn \
  scipy \
  six \
  s3fs \
  ujson \
  xlrd
