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
from setuptools import setup


setup(
    name='{{cookiecutter.package_name}}',
    version='0.0.1',
    description='A PySpark Cloud project, generated from cookiecutter-pyspark-cloud.',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3.6',
    ],
    author='Daniel Cortez Stevenson',
    author_email='daniel@jyde.io',
    license='Apache',
    packages=['{{ cookiecutter.package_name }}'],
    install_requires=[
        'findspark',
    ],
    setup_requires=[
        'pytest-runner >=2.0,<3dev',
    ],
    tests_require=[
        'pytest',
        'pytest-spark',
    ],
    include_package_data=True,
    package_data={
        '*': [
            '*.csv',
            '*.yml',
            '*.yaml',
            '*.sh',
        ],
    },
    entry_points={
        'console_scripts': [
            '{{ cookiecutter.package_name }} = {{ cookiecutter.package_name }}.cli:main',
        ],
    },
    extras_require={
        'client': [
            'awscli',
            'boto3',
            'click >=7.0.',
            'daiquiri',
            'pyfiglet ==0.8.post1',
        ],
        'dev': [
            'bump2version',
            'flake8',
            'mypy',
            'pyspark-stubs',
            's3cmd',
            'yamllint',
        ],
        'spark': [
            'pyspark ==2.4.4',
        ],
        'spark-node': [
            'boto3',
        ],
    },
    zip_safe=True,
)
