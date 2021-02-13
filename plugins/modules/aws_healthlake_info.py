#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_healthlake_info
short_description: Get Information about Amazon Health Lake.
description:
  - Get Information about Amazon Health Lake.
  - U(https://docs.aws.amazon.com/healthlake/latest/APIReference/API_Operations.html)
version_added: 0.0.6
options:
  id:
    description:
      - id of fhir datastore.
    required: false
    type: str
  job_id:
    description:
      - can be id of export job or import job?
    required: false
    type: str
  datastore_status:
    description:
      - status of datastore to filter results.
    required: false
    type: str
    choices: ['CREATING', 'ACTIVE', 'DELETING', 'DELETED']
    default: 'ACTIVE'
  list_fhir_datastores:
    description:
      - do you want to get list of fhir_datastores?
    required: false
    type: bool
  describe_fhir_datastore:
    description:
      - do you want to get details of fhir_datastore for given I(id)?
    required: false
    type: bool
  describe_fhir_export_job:
    description:
      - do you want to get details export job for given I(id) and I(job_id)?
    required: false
    type: bool
  describe_fhir_import_job:
    description:
      - do you want to get details import job for given I(id) and I(job_id)
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
- name: "get list of fhir_datastores"
  aws_healthlake_info:
    list_fhir_datastores: true
    datastore_status: 'ACTIVE'

- name: "get details of fhir_datastore"
  aws_healthlake_info:
    describe_fhir_datastore: true
    id: 'test'

- name: "get details of fhir_export_job"
  aws_healthlake_info:
    describe_fhir_export_job: true
    id: 'test-datastore-id'
    job_id: 'test'

- name: "get details of fhir_import_job"
  aws_healthlake_info:
    describe_fhir_import_job: true
    id: 'test-datastore-id'
    job_id: 'test'
"""

RETURN = """
fhir_datastores:
  description: list of fhir_datastores.
  returned: when `list_fhir_datastores` is defined and success.
  type: list
fhir_datastore:
  description: details of fhir_datastore.
  returned: when `describe_fhir_datastore` is defined and success.
  type: dict
fhir_export_job:
  description: list of fhir_export_job.
  returned: when `describe_fhir_export_job` is defined and success.
  type: dict
fhir_import_job:
  description: list of fhir_import_job.
  returned: when `describe_fhir_import_job` is defined and success.
  type: dict
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser
from ansible.module_utils.common.dict_transformations import camel_dict_to_snake_dict


def _healthlake(client, module):
    try:
        if module.params['list_fhir_datastores']:
            if client.can_paginate('list_fhir_datastores'):
                paginator = client.get_paginator('list_fhir_datastores')
                return paginator.paginate(
                    Filter={
                        "DatastoreStatus": module.params['datastore_status'],
                    }
                ), True
            else:
                return client.list_fhir_datastores(
                    Filter={
                        "DatastoreStatus": module.params['datastore_status'],
                    }
                ), False
        elif module.params['describe_fhir_datastore']:
            return client.describe_fhir_datastore(
                DatastoreId=module.params['id']
            ), False
        elif module.params['describe_fhir_export_job']:
            return client.describe_fhir_export_job(
                DatastoreId=module.params['id'],
                JobId=module.params['job_id']
            ), False
        elif module.params['describe_fhir_import_job']:
            return client.describe_fhir_import_job(
                DatastoreId=module.params['id'],
                JobId=module.params['job_id']
            ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon healthlake details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['datastore_id']),
        job_id=dict(required=False),
        datastore_status=dict(required=False, choices=['CREATING', 'ACTIVE', 'DELETING', 'DELETED'], default='ACTIVE'),
        list_fhir_datastores=dict(required=False, type=bool),
        describe_fhir_datastore=dict(required=False, type=bool),
        describe_fhir_export_job=dict(required=False, type=bool),
        describe_fhir_import_job=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('describe_fhir_datastore', True, ['id']),
            ('describe_fhir_export_job', True, ['id', 'job_id']),
            ('describe_fhir_import_job', True, ['id', 'job_id']),
        ),
        mutually_exclusive=[
            (
                'list_fhir_datastores',
                'describe_fhir_datastore',
                'describe_fhir_export_job',
                'describe_fhir_import_job',
            )
        ],
    )

    client = module.client('healthlake', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _healthlake(client, module)

    if module.params['list_fhir_datastores']:
        module.exit_json(fhir_datastores=aws_response_list_parser(paginate, it, 'DatastorePropertiesList'))
    elif module.params['describe_fhir_datastore']:
        module.exit_json(fhir_datastore=camel_dict_to_snake_dict(it))
    elif module.params['describe_fhir_export_job']:
        module.exit_json(fhir_export_job=camel_dict_to_snake_dict(it['ExportJobProperties']))
    elif module.params['describe_fhir_import_job']:
        module.exit_json(fhir_import_job=camel_dict_to_snake_dict(it['ImportJobProperties']))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
