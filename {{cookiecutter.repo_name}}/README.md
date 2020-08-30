# {{cookiecutter.repo_name}}

A 'starter-kit' for PySpark in the cloud :cloud: - from infrastructure to spark-submit call.

## Quickstart

```
conda create -n {{cookiecutter.repo_name}} -y "python=3.6"
conda activate {{cookiecutter.repo_name}}

make install

{{cookiecutter.package_name}}
```

## Usage

### Install a Python 3.6 Environment

```
conda create -n {{cookiecutter.repo_name}} -y "python=3.6"
conda activate {{cookiecutter.repo_name}}
```

### Install {{cookiecutter.package_name}} for Development

```
make install-dev
```

### Test the Python package

```
make test
```

### AWS

#### Store Data and Assets in S3

```
aws s3 mb s3://{{cookiecutter.s3_bucket}}
```

#### Deploy Infrastrucutre as Code with AWS Cloudformation

Distribute code:

*make cluster bootstrap & EMR Step API bash scripts, PySpark code available via S3*

```
make s3dist
```

Make Keys:

*create the necessary AWS EC2 Key Pairs for the bastion server and master node via the AWS Console*

Example Key Pair Names:

- test-{{cookiecutter.repo_name}}-bastion

- test-{{cookiecutter.repo_name}}-emr

Deploy infrastructure:

```
aws cloudformation create-stack \
    --stack-name "{{cookiecutter.project_name | slugify(separator='')}}-{{random_ascii_string(6) | lower}}" \
    --template-body file://./cloudformation/emr-template.yaml \
    --tags Key=Environment,Value=Test Key=Project,Value={{cookiecutter.project_name | slugify(separator='')}} \
    --timeout-in-minutes 30 \
    --parameters \
        ParameterKey=BastionKeyName,ParameterValue=test-{{cookiecutter.repo_name}}-bastion \
        ParameterKey=EmrKeyName,ParameterValue=test-{{cookiecutter.repo_name}}-emr \
    # --disable-rollback  # uncomment this line for debugging the stack deployment
```

#### Submit PySpark code as AWS EMR Steps using the `{{cookiecutter.package_name}}` CLI

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
    -i *your-emr-cluster-id* \
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
    -i *your-emr-cluster-id* \
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
    ssh -i /path/to/your/bastion/keyfile.pem -ND 8157 ec2-user@*your-bastion-dns*
    ```

3. Access JupterHub at port `9443` of your Master Public DNS Name (exported from Cloudformation Template)

    - [Reference](https://docs.aws.amazon.com/emr/latest/ReleaseGuide/emr-jupyterhub-connect.html)

## Contributing

### How to add a new `job`

1. Add a *.py file in the {{cookiecutter.package_name}}/job/ [`job` directory]({{cookiecutter.package_name}}/job/).

2. Add a function signature for the job, like so:

    - `spark` must be the first argument
    - reasonable to also insert `**kwargs` as the last argument

    ```python
    def main(spark, arg1, arg2, ..., **kwargs):
        # Your PySpark code here!
        return None
    ```

### Tagging & Versioning

Use [`bump2version`](https://github.com/c4urself/bump2version) to create a new version commit and tag it:

```
bumpversion patch  # major | minor | patch
git push --tags
```
