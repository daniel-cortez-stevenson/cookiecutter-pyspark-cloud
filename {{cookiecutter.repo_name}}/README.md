# {{cookiecutter.repo_name}}

A PySpark on EMR stater kit - from infrastructure to spark-submit call.

## How to use this repo

### Install Python libs

```
conda create -n {{cookiecutter.repo_name}} -y "python=3.6"
source activate {{cookiecutter.repo_name}}
make install-dev
```

### Create your S3 bucket

```
aws s3 mb s3://{{cookiecutter.package_name}}
```

### Deploy the AWS Cloud :cloud: Infrastrucutre as Code with AWS Cloudformation

Distribute your EMR bootstrap / step scripts and Python package via S3:

```
make s3dist
```

```
aws cloudformation create-stack \
    --stack-name MyEmrTestXyz123 \
    --template-body file://./cloudformation/emr-template.yaml \
    --tags Key=Environment,Value=Test Key=Project,Value=MyPySparkProject \
    --parameters \
        ParameterKey=BastionKeyName,ParameterValue=test-pyspark-aws-emr-bastion \
        ParameterKey=EmrKeyName,ParameterValue=test-pyspark-aws-emr-emr \
    # for debugging the stack use `--disable-rollback`
```

### Submit PySpark code as AWS EMR Steps using the `{{cookiecutter.package_name}}` CLI

Get help:

```
{{cookiecutter.package_name}} --help
```

List EMR Cluster IDs :

```
{{cookiecutter.package_name}} list emr
```

Submit job module PySpark code to AWS EMR as a Step:

```
{{cookiecutter.package_name}} job \
    -i *your-emr-cluster-id*
    -s ExampleOneStep \
    -b {{cookiecutter.s3_bucket}} \
    -p "dist/" \
    -j example_one \
    "bucket={{cookiecutter.s3_bucket}}" \
    "prefix=dist/" \
    "suffix=.py"
```

Another example:

```
{{cookiecutter.package_name}} job \
    -i *your-emr-cluster-id*
    -s ExampleTwoStep \
    -b {{cookiecutter.s3_bucket}} \
    -p "dist/" \
    -P "com.github.master:spark-stemming_2.10:0.2.1" \
    -j example_two
```

### Access JupyterHub by Port-Forwarding through the Bastion Server

See [this Blog Post for port-forwarding instructions](https://bytes.babbel.com/en/articles/2017-07-04-spark-with-jupyter-inside-vpc.html)

tl;dr

1. Set up an in-browser proxy extension like [Proxy SwitchyOmega](https://chrome.google.com/webstore/detail/proxy-switchyomega/padekgcemlokbadohgkifijomclgjgif?hl=en).

    - Settings:
        - Protocol: `SOCKS5`
        - Server: `localhost`
        - Port: `8157`

2. Start port-forwarding from bash:

    ```
    ssh -ND 8157 bastion
    ```

3. Access JupterHub at port `9443` of your Master Public DNS Name (exported from Cloudformation Template)

    - [Reference](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-jupyterhub-connect.html)

## Development

1. Write PySpark code in the body of the `main` function in a new Python module (*.py file) in [the`job` module]({{cookiecutter.package_name}}/job/).

    - `spark` must be the first argument
    - reasonable to also insert `**kwargs` as the last argument
    
2. Distribute your code:

    ```
    {{cookiecutter.package_name}} s3dist
    ```
