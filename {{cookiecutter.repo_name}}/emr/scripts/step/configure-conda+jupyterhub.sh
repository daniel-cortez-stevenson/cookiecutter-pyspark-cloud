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
# Run on AWS EMR master node w/ JupyterHub Application
# Configures Conda and installs Python libs
#
# Usage:
#   sh configure-conda+jupyterhub.sh

set -x -e

/usr/bin/sudo /usr/bin/docker exec jupyterhub bash -c """
set -x -e

apt-get update -y && apt-get install -y \
    git \
    zip

pip install -U pip

pip install -U -q \
    dash==1.0.0 \
    dash-daq==0.1.0 \
    https://s3.amazonaws.com/h2o-release/datatable/stable/datatable-0.8.0/datatable-0.8.0-cp36-cp36m-linux_x86_64.whl \
    plotly \
    seaborn

jupyter serverextension enable --py --system sparkmagic
jupyter nbextension enable --py --system widgetsnbextension
"""
