#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_glacier_info
short_description: Get Information about Amazon Glacier.
description:
  - Get Information about Amazon Glacier.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/glacier.html)
version_added: 0.0.6
options:
  name:
    description:
      - name of vault.
    required: false
    type: str
  status:
    description:
      - status of vault job.
    required: false
    type: str
    choices: ['InProgress', 'Succeeded', 'Failed']
    default: 'Succeeded'
  list_vaults:
    description:
      - do you want to get list of vaults?
    required: false
    type: bool
  list_provisioned_capacity:
    description:
      - do you want to get list of provisioned capacity?
    required: false
    type: bool
  list_multipart_uploads:
    description:
      - do you want to get list of multipart uploads for given I(name)?
    required: false
    type: bool
  list_jobs:
    description:
      - do you want to get list of jobs for given I(name)?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
extends_documentation_fragment:
  - amazon.aws.ec2
  - amazon.aws.aws
requirements:
  - boto3
  - botocore
"""

EXAMPLES = """
- name: "get details of vaults"
  aws_glacier_info:
    list_vaults: true

- name: "get details of provisioned capacity"
  aws_glacier_info:
    list_provisioned_capacity: true

- name: "get details of multipart uploads"
  aws_glacier_info:
    list_multipart_uploads: true
    name: 'test'

- name: "get details of jobs"
  aws_glacier_info:
    list_jobs: true
    name: 'test'
    status: 'Succeeded'

"""

RETURN = """
vaults:
  description: list of vaults.
  returned: when `list_vaults` is defined and success.
  type: list
provisioned_capacity:
  description: list of provisioned capacity.
  returned: when `list_provisioned_capacity` is defined and success.
  type: list
multipart_uploads:
  description: list of multipart uploads.
  returned: when `list_multipart_uploads` is defined and success.
  type: list
jobs:
  description: list of jobs.
  returned: when `list_jobs` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _glacier(client, module):
    try:
        if module.params['list_vaults']:
            if client.can_paginate('list_vaults'):
                paginator = client.get_paginator('list_vaults')
                return paginator.paginate(), True
            else:
                return client.list_vaults(), False
        elif module.params['list_provisioned_capacity']:
            if client.can_paginate('list_provisioned_capacity'):
                paginator = client.get_paginator('list_provisioned_capacity')
                return paginator.paginate(), True
            else:
                return client.list_provisioned_capacity(), False
        elif module.params['list_multipart_uploads']:
            if client.can_paginate('list_multipart_uploads'):
                paginator = client.get_paginator('list_multipart_uploads')
                return paginator.paginate(
                    vaultName=module.params['name'],
                ), True
            else:
                return client.list_multipart_uploads(
                    vaultName=module.params['name'],
                ), False
        elif module.params['list_jobs']:
            if client.can_paginate('list_jobs'):
                paginator = client.get_paginator('list_jobs')
                return paginator.paginate(
                    vaultName=module.params['name'],
                    statuscode=module.params['status'],
                ), True
            else:
                return client.list_jobs(
                    vaultName=module.params['name'],
                    statuscode=module.params['status'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon glacier details')


def main():
    argument_spec = dict(
        status=dict(required=False, choices=['InProgress', 'Succeeded', 'Failed'], default='Succeeded'),
        name=dict(required=False),
        list_vaults=dict(required=False, type=bool),
        list_provisioned_capacity=dict(required=False, type=bool),
        list_multipart_uploads=dict(required=False, type=bool),
        list_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_multipart_uploads', True, ['name']),
            ('list_jobs', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_vaults',
                'list_provisioned_capacity',
                'list_multipart_uploads',
                'list_jobs',
            )
        ],
    )

    client = module.client('glacier', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _glacier(client, module)

    if module.params['list_vaults']:
        module.exit_json(vaults=aws_response_list_parser(paginate, it, 'VaultList'))
    elif module.params['list_provisioned_capacity']:
        module.exit_json(provisioned_capacity=aws_response_list_parser(paginate, it, 'ProvisionedCapacityList'))
    elif module.params['list_multipart_uploads']:
        module.exit_json(multipart_uploads=aws_response_list_parser(paginate, it, 'UploadsList'))
    elif module.params['list_jobs']:
        module.exit_json(jobs=aws_response_list_parser(paginate, it, 'JobList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
