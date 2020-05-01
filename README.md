# cookiecutter-pyspark-aws-emr

Get started on AWS EMR with this [cookiecutter](https://cookiecutter.readthedocs.io/en/1.7.2/usage.html) template!

## Quickstart

1. Create a Python environment with cookiecutter installed:

```
conda create -n cookiecutter -y "python=3.7" cookiecutter
conda activate cookiecutter
```

2. Git clone this repo, and make your changes:

```
git clone https://github.com/daniel-cortez-stevenson/cookiecutter-pyspark-aws-emr.git
# make any changes you wish to locally
```

3. Create your repo from this template:

```
cookiecutter ./cookiecutter-pyspark-aws-emr
```

## Features

- AWS Clouformation Template for EMR: Simple Spark cluster deployment with infrastructure as code

    - [JupyterHub](https://jupyterhub.readthedocs.io/en/stable/) is installed to the EMR Master node for development.

- Simplify Workflows with Make: A Makefile with commands for installation and deployment

    - Installation for regular-use and development
    - Package and deploy your code to AWS S3

- A Command-Line Interface for Running PySpark 'Jobs': For Production runs via EMR Step API.

    - Uses the concept of 'jobs', which run PySpark scripts as a Python function via a common entrypoint.

- Reduce Duplication in Your PySpark Code: Package code shared between 'jobs' in a Python module of your package
 called `common`

- Wrap Scala with Python: An example of wrapping Scala Spark API code with PySpark API code is provided with
 `SnowballStemmer`
 
- Extend the PySpark API: An example of extending the PySpark SQL `DataFrame` class, which allows chaining custom
 transformations with dot `.` notation
 
- Development Framework: Use [bump2version](https://github.com/c4urself/bump2version) to version your project.
 
## Contribute

Contributions are welcome! 

- [Submit an Issue](https://github.com/daniel-cortez-stevenson/cookiecutter-pyspark-aws-emr/issues/new)

- [Submit a Pull Request](https://github.com/daniel-cortez-stevenson/cookiecutter-pyspark-aws-emr/compare)