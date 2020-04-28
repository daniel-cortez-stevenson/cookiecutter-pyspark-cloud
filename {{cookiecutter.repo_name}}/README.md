# {{cookiecutter.repo_name}}

A PySpark on EMR stater kit - from infrastructure set up to spark-submit call.

## How to use this repo

### Install Python libs

```
conda create -n {{cookiecutter.repo_name}} -y "python=3.6"
source activate {{cookiecutter.repo_name}}
make install-dev
```

### Create a Python distribution

Upload the .egg files to s3

```
make s3dist -bucket {{cookiecutter.s3_bucket}}
```

### Deploy the AWS Cloud :cloud: Infrastrucutre as Code with Cloudformation

```
aws cloudformation create-stack \
     --template-file file://./cloudformation/vpc-s3-nat-emr.yml  # ... WIP
```

### Use the CLI to Submit PySpark code as AWS EMR Steps

```
{{cookiecutter.package_name}} --help
```

### Access JupyterHub by Port-Forwarding through the Bastion Server

See [this Blog Post for port-forwarding instructions](https://bytes.babbel.com/en/articles/2017-07-04-spark-with-jupyter-inside-vpc.html)

## Development

1. Write PySpark code in the body of the `main` function in a new Python module (*.py file) in [the`job` module]({{cookiecutter.package_name}}/job/). 

    - `spark` must be the first argument
    - reasonable to also insert `**kwargs` as the last argument
    
2. Build your Python package into a foldr called 'dist' and upload it to S3.

3. Use the CLI to run your job:

```
# WIP
```
