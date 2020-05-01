"""Client-side Command Line Interface for PySpark on AWS EMR

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
import logging
from os.path import join

import boto3
import click
import pyfiglet

from {{cookiecutter.package_name}} import __version__


logger = logging.getLogger(__name__)

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
ACTIONS_ON_FAILRE = ['TERMINATE_JOB_FLOW', 'CANCEL_AND_WAIT', 'CONTIUNUE']


def main():
    cli()


@click.group(invoke_without_command=True, context_settings=CONTEXT_SETTINGS)
@click.pass_context
def cli(ctx):
    if not ctx.invoked_subcommand:
        f = pyfiglet.Figlet(font='slant')
        click.echo(f.renderText('{{cookiecutter.package_name}}'))
        click.echo(f'v{__version__}')


@cli.command(context_settings=dict(ignore_unknown_options=True, allow_extra_args=True, **CONTEXT_SETTINGS),
             short_help='Submit PySpark code as an EMR Step.')
@click.option('-i', '--cluster-id', required=True, help='EMR Cluster ID - also called Job Flow ID.')
@click.option('-s', '--step-name', required=True, help='Give your EMR Step a descriptive name.')
@click.option('-b', '--bucket', required=True, help='S3 bucket that contians the egg distribution.')
@click.option('-p', '--prefix', required=True, help='S3 prefix that contains the egg distribution.')
@click.option('-P', '--packages', required=False, help='Spark package dependencies of the job.')
@click.option('-A', '--action-on-failure', default='TERMINATE_JOB_FLOW', type=click.Choice(ACTIONS_ON_FAILRE),
              help='Keyword specifying EMR behavior if the Step fails.')
@click.option('-j', '--job-name', required=True, help='The name of the job module to run.')
@click.argument('job-kwargs', nargs=-1)
@click.pass_context
def job(ctx, cluster_id, step_name, bucket, prefix, packages, action_on_failure, job_name, job_kwargs):
    """Submit a PySpark job via the AWS EMR Step API.

    [ARGS]

    JOB_KWARGS = Unlimited number of '=' separated keyword / argument value
        pairs to the --job-name`main` function. Ex. "arg1=val1" "arg2=arg2" ...
    """
    # Get Python code assets from S3
    distribution_prefix = join('s3://', bucket, prefix, 'dist')
    egg_key = join(distribution_prefix, 'spotlight-' + __version__ + '-py3.6.egg')
    pyspark_entrypoint_key = join(distribution_prefix, 'pyspark_entrypoint.py')

    # Build the arguments to send to command-runner.jar
    spark_submit_cmd = ['spark-submit']
    if packages:
        spark_submit_cmd.extend(['--packages', packages])
    spark_submit_cmd.extend(['--py-files', egg_key])
    spark_submit_cmd.append(pyspark_entrypoint_key)
    spark_submit_cmd.extend(['--job-name', job_name])
    if job_kwargs:
        spark_submit_cmd.extend(['--job-kwargs'] + list(job_kwargs))
    msg = f'Will execute the following spark-submit command on EMR Master:\n\t{spark_submit_cmd}\n\n'
    click.echo(msg)

    # Submit the EMR Step through the API
    client = boto3.client('emr')
    response = client.add_job_flow_steps(
        JobFlowId=cluster_id,
        Steps=[
            {
                'Name': step_name,
                'ActionOnFailure': action_on_failure,
                'HadoopJarStep': {
                    'Jar': 'command-runner.jar',
                    'Args': spark_submit_cmd,
                },
            },
        ],
    )
    click.echo(response)


@cli.group('list', context_settings=CONTEXT_SETTINGS, short_help='Get deployment info')
@click.pass_context
def list_(ctx):
    pass


@list_.command('emr', context_settings=CONTEXT_SETTINGS, short_help='List available AWS EMR cluster IDs')
@click.pass_context
def list_emr(ctx):
    emr = boto3.client('emr')
    clusters = emr.list_clusters(
        ClusterStates=[
            'STARTING', 'BOOTSTRAPPING', 'RUNNING', 'WAITING',
        ],
    )['Clusters']
    click.echo(clusters)


if __name__ == '__main__':
    main()
