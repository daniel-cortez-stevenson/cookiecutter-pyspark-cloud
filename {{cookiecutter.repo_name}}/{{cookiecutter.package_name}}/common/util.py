"""Utilities for your PySpark ETL.

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

import boto3


logger = logging.getLogger(__name__)


def list_s3_keys(bucket: str,
                 prefix: str,
                 suffix: str,
                 pagination_conf: dict = None) -> 'List[str]':
    """List AWS S3 keys efficiently so PySpark does not have to do an expensive
    recursive list operation.

    Args:
        bucket (str): AWS S3 bucket name.
        prefix (str): Only list S3 keys starting with this value.
        suffix (str): Only list S3 keys ending with this value.
        pagination_conf (dict): Control how the S3 list_objects_v2 response is
            paginated. Default is `{'PageSize': None, 'MaxItems': None}`, which
            uses the AWS boto3 API defaults.

    Returns:
        List[str]. S3 keys in bucket with prefix and suffix.
    """
    s3_list_paginator = boto3.client('s3').get_paginator('list_objects_v2')

    pagination_conf = pagination_conf or {'PageSize': None, 'MaxItems': None}

    try:
        response = s3_list_paginator.paginate(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter='',
            PaginationConfig=pagination_conf,
        )
        logger.debug(f'Response: {response}')
    except Exception:
        raise  # FIXME: Specify Errors and handle appropriately

    keys = []

    for page in response:
        if 'Contents' in page:
            for content in page['Contents']:
                try:
                    key = content['Key']
                    if key and key.endswith(suffix):
                        keys.append(key)
                except KeyError:
                    pass
    logger.info(f'Found S3 keys: {keys}')
    return keys
