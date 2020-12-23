#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_backup_info
short_description: Get Information about AWS Backup.
description:
  - Get Information about AWS Backup.
  - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_Operations.html)
version_added: 1.4.0
options:
  backup_plan_id:
    description:
      - Id of Backup Plan.
      - >
        Mutually Exclusive with I(list_backup_plans_include_deleted), I(list_backup_plan_templates).
        I(list_backup_vaults), I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: str
  list_backup_plans_include_deleted:
    description:
      - do you want to include deleted backup plans?
      - >
        Mutually Exclusive with I(list_backup_plans_include_deleted), I(list_backup_plan_templates).
        I(list_backup_vaults), I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_plan_templates:
    description:
      - do you want to fetch backup plan templates?
      - >
        Mutually Exclusive with I(list_backup_plans_include_deleted), I(list_backup_plan_templates).
        I(list_backup_vaults), I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_vaults:
    description:
      - do you want to fetch list of backup vaults?
      - >
        Mutually Exclusive with I(list_backup_plans_include_deleted), I(list_backup_plan_templates).
        I(list_backup_vaults), I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_selections:
    description:
      - do you want to fetch backup selections?
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupSelections.html)
      - >
        Mutually Exclusive with I(list_backup_selections), I(list_backup_plan_versions)
        I(list_backup_plans_include_deleted), I(list_backup_plan_templates), I(list_backup_vaults)
        I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_plan_versions:
    description:
      - do you want to fetch backup plan versions?
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupPlanVersions.html)
      - >
        Mutually Exclusive with I(list_backup_selections), I(list_backup_plan_versions)
        I(list_backup_plans_include_deleted), I(list_backup_plan_templates), I(list_backup_vaults)
        I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_jobs:
    description:
      - do you want to fetch backup jobs?
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
      - >
        Mutually Exclusive with I(list_backup_selections), I(list_backup_plan_versions)
        I(list_backup_plans_include_deleted), I(list_backup_plan_templates), I(list_backup_vaults)
        I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_backup_jobs_by_resource_arn:
    description:
      - fetch backup jobs by resource arn.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
    required: false
    type: str
  list_backup_jobs_by_state:
    description:
      - fetch backup jobs by job state.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
    required: false
    type: str
  list_backup_jobs_by_backup_vault_name:
    description:
      - fetch backup jobs by backup vault name.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
    required: false
    type: str
  list_backup_jobs_by_resource_type:
    description:
      - fetch backup jobs by resource type used in backup job.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
    required: false
    type: str
  list_backup_jobs_by_account_id:
    description:
      - fetch backup jobs by account id used in backup job.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html)
    required: false
    type: str
  list_copy_jobs:
    description:
      - do you want to fetch backup copy jobs?
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
      - >
        Mutually Exclusive with I(list_backup_selections), I(list_backup_plan_versions)
        I(list_backup_plans_include_deleted), I(list_backup_plan_templates), I(list_backup_vaults)
        I(list_backup_jobs) and I(list_copy_jobs)
    required: false
    type: bool
  list_copy_jobs_by_resource_arn:
    description:
      - fetch backup copy jobs by resource arn.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
    required: false
    type: str
  list_copy_jobs_by_state:
    description:
      - fetch backup copy jobs by state of job.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
    required: false
    type: str
  list_copy_jobs_by_resource_type:
    description:
      - fetch backup copy jobs by resource type.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
    required: false
    type: str
  list_copy_jobs_by_account_id:
    description:
      - fetch backup copy jobs by account id.
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
    required: false
    type: bool
  list_copy_jobs_by_destination_vault_arn:
    description:
      - fetch backup copy jobs by destination vault arn?
      - U(https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html)
    required: false
    type: str
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
- name: "get list of aws backup plans without deleted plans"
  aws_backup_info:

- name: "get list of aws backup plans with deleted plans"
  aws_backup_info:
    list_backup_plans_include_deleted: true

- name: "get basic details about specific backup plan"
  aws_backup_info:
    backup_plan_id: "{{ __b.backup_plans[0].backup_plan_id }}"
    list_backup_selections: true

- name: "get list of backup plan versions about specific backup plan"
  aws_backup_info:
    backup_plan_id: "{{ __b.backup_plans[0].backup_plan_id }}"
    list_backup_plan_versions: true

- name: "get list of backup plan templates"
  aws_backup_info:
    list_backup_plan_templates: true

- name: "get list of backup vaults"
  aws_backup_info:
    list_backup_vaults: true

- name: "get list of backup jobs for given backup vault name"
  aws_backup_info:
    list_backup_jobs: true
    list_backup_jobs_by_backup_vault_name: 'rds-valut'

- name: "list of backup jobs for given vault name and state"
  aws_backup_info:
    list_backup_jobs: true
    list_backup_jobs_by_backup_vault_name: 'rds-valut'
    list_backup_jobs_by_state: 'COMPLETED'

- name: "list of backup copy jobs"
  aws_backup_info:
    list_copy_jobs: true
    list_copy_jobs_by_state: 'COMPLETED'
"""

RETURN = """
backup_plans:
  description: List of backup plans.
  returned: when no argument is defined or `list_backup_plans_include_deleted` and success
  type: list
  sample: [
    {
        "backup_plan_arn": "arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b",
        "backup_plan_id": "55934731-xxxxx-a4a44b98f40b",
        "backup_plan_name": "test-rds-backup",
        "creation_date": "2020-11-16T16:08:15.039000+02:00",
        "last_execution_date": "2020-12-23T01:14:33.406000+02:00",
        "version_id": "ODJhZDFhxxxxxxxxxA5ZGYyZDgx"
    },
    {
        "backup_plan_arn": "arn:aws:backup:us-east-1:xxxxx:backup-plan:74a37778-xxxxx-9176d22ae8f2",
        "backup_plan_id": "74a37778-xxxxx-9176d22ae8f2",
        "backup_plan_name": "Test",
        "creation_date": "2020-10-13T15:39:45.605000+03:00",
        "deletion_date": "2020-10-13T16:58:10.741000+03:00",
        "last_execution_date": "2020-10-13T16:33:12.037000+03:00",
        "version_id": "Yzk2YWJmMTxxxxxFkNTNmNTRm"
    }
  ]
backup_plan_selections:
  description: List of backup plans selections.
  returned: when `backup_plan_id`, `list_backup_selections` and success
  type: list
  sample: [
    {
        "backup_plan_id": "55934731-xxxxx-a4a44b98f40b",
        "creation_date": "2020-11-16T14:33:42.554000+02:00",
        "creator_request_id": "8dd55ad7-xxx-47edc804e3d3",
        "iam_role_arn": "arn:aws:iam::xxxxx:role/service-role/AWSBackupDefaultServiceRole",
        "selection_id": "06c9f85f-c49e-4efb-ace3-b1fd1ef86862",
        "selection_name": "test-rds"
    }
  ]
backup_plan_versions:
  description: List of backup plans versions.
  returned: when `backup_plan_id`, `list_backup_plan_versions` and success
  type: list
  sample: [
    {
        "backup_plan_arn": "arn:aws:backup:us-east-1:xxxxx:backup-plan:55934731-xxxxx-a4a44b98f40b",
        "backup_plan_id": "55934731-xxxxx-a4a44b98f40b",
        "backup_plan_name": "test-rds-backup",
        "creation_date": "2020-11-16T16:08:15.039000+02:00",
        "last_execution_date": "2020-12-23T01:14:33.406000+02:00",
        "version_id": "ODJhZDFhOWItYxxxxxxxYjA5ZGYyZDgx"
    },
    {
        "backup_plan_arn": "arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b",
        "backup_plan_id": "55934731-xxxxx-a4a44b98f40b",
        "backup_plan_name": "test-rds-backup",
        "creation_date": "2020-11-16T14:55:46.131000+02:00",
        "deletion_date": "2020-11-16T16:08:15.039000+02:00",
        "last_execution_date": "2020-11-16T16:07:47.272000+02:00",
        "version_id": "ZDliN2U5YjMxxxxxI1NmU4Y2U1MDk5"
    }
  ]
backup_plan_templates:
  description: List of backup plans templates.
  returned: when `list_backup_plan_templates` and success
  type: list
  sample: [
    {
        "backup_plan_template_id": "87c0c1ef-xxxxxx-2e76a2c38aaa",
        "backup_plan_template_name": "Daily-35day-Retention"
    },
    {
        "backup_plan_template_id": "87c0c1ef-xxxxxx-2e76a2c38aab",
        "backup_plan_template_name": "Daily-Monthly-1yr-Retention"
    }
  ]
backup_vaults:
  description: List of backup vaults.
  returned: when `list_backup_vaults` and success
  type: list
  sample: [
    {
        "backup_vault_arn": "arn:aws:backup:us-east-1:xxxx:backup-vault:Default",
        "backup_vault_name": "Default",
        "creation_date": "2019-01-28T10:31:25.594000+02:00",
        "creator_request_id": "Default",
        "encryption_key_arn": "arn:aws:kms:us-east-1:xxxx:key/8308c521-xxxxx-86bda5017bf4",
        "number_of_recovery_points": 0
    }
  ]
backup_jobs:
  description: List of backup jobs.
  returned: >
    when `list_backup_jobs` and any filter values are passed like
    `list_backup_jobs_by_backup_vault_name`, `list_backup_jobs_by_state`
    `list_backup_jobs_by_resource_arn`, `list_backup_jobs_by_resource_type`
    `list_backup_jobs_by_account_id`
    and success
  type: list
  sample: [
    {
        "account_id": "xxxx",
        "backup_job_id": "9AA49310-xxxx-6B3522195FDB",
        "backup_size_in_bytes": 0,
        "backup_vault_arn": "arn:aws:backup:us-east-1:xxx:backup-vault:rds-valut",
        "backup_vault_name": "rds-valut",
        "completion_date": "2020-12-23T01:28:05.634000+02:00",
        "created_by": {
            "backup_plan_arn": "arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b",
            "backup_plan_id": "55934731-xxxxx-a4a44b98f40b",
            "backup_plan_version": "ODJhZDFhOWIxxxxxxxYjA5ZGYyZDgx",
            "backup_rule_id": "8430c4d0-xxxxxxxxx-54c449719284"
        },
        "creation_date": "2020-12-23T01:14:33.406000+02:00",
        "iam_role_arn": "arn:aws:iam::xxxxxx:role/service-role/AWSBackupDefaultServiceRole",
        "percent_done": "100.0",
        "recovery_point_arn": "arn:aws:rds:us-east-1:xxxxxxx:snapshot:awsbackup:job-9aa49310-xxxxx-6b3522195fdb",
        "resource_arn": "arn:aws:rds:us-east-1:xxxxxxxxxxx:db:test",
        "resource_type": "RDS",
        "start_by": "2020-12-23T02:10:00+02:00",
        "state": "COMPLETED"
    }
  ]
copy_jobs:
  description: List of backup copy jobs.
  returned: >
    when `list_copy_jobs` and any filter values are passed like
    `list_copy_jobs_by_state`, `list_copy_jobs_by_resource_arn`,
    `list_copy_jobs_by_resource_type`, `list_copy_jobs_by_account_id`
    `list_copy_jobs_by_destination_vault_arn`
    and success
  type: list
  sample: [
    {
        'account_id': 'string',
        'copy_job_id': 'string',
        'source_backup_vault_arn': 'string',
        'source_recovery_point_arn': 'string',
        'destination_backup_vault_arn': 'string',
        'destination_recovery_point_arn': 'string',
        'resource_arn': 'string',
        'creation_date': datetime(2015, 1, 1),
        'completion_date': datetime(2015, 1, 1),
        'state': 'CREATED'|'RUNNING'|'COMPLETED'|'FAILED',
        'status_message': 'string',
        'backup_size_in_bytes': 123,
        'iam_role_arn': 'string',
        'created_by': {
            'backup_plan_id': 'string',
            'backup_plan_arn': 'string',
            'backup_plan_version': 'string',
            'backup_rule_id': 'string'
        },
        'resource_type': 'string'
    }
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
# from datetime import datetime


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _backup(module):
    try:
        backup = module.client('backup')

        if module.params['list_backup_selections']:
            if backup.can_paginate('list_backup_selections'):
                paginator = backup.get_paginator('list_backup_selections')
                return paginator.paginate(
                    BackupPlanId=module.params['backup_plan_id']
                ), True
            else:
                return backup.list_backup_selections(
                    BackupPlanId=module.params['backup_plan_id']
                ), False
        elif module.params['list_backup_plan_versions']:
            if backup.can_paginate('list_backup_plan_versions'):
                paginator = backup.get_paginator('list_backup_plan_versions')
                return paginator.paginate(
                    BackupPlanId=module.params['backup_plan_id']
                ), True
            else:
                return backup.list_backup_plan_versions(
                    BackupPlanId=module.params['backup_plan_id']
                ), False
        elif module.params['list_backup_plan_templates']:
            if backup.can_paginate('list_backup_plan_templates'):
                paginator = backup.get_paginator('list_backup_plan_templates')
                return paginator.paginate(), True
            else:
                return backup.list_backup_plan_templates(), False
        elif module.params['list_backup_vaults']:
            if backup.can_paginate('list_backup_vaults'):
                paginator = backup.get_paginator('list_backup_vaults')
                return paginator.paginate(), True
            else:
                return backup.list_backup_vaults(), False
        elif module.params['list_backup_jobs']:
            if backup.can_paginate('list_backup_jobs'):
                paginator = backup.get_paginator('list_backup_jobs')
                return paginator.paginate(
                    ByResourceArn=module.params['list_backup_jobs_by_resource_arn'],
                    ByState=module.params['list_backup_jobs_by_state'],
                    ByBackupVaultName=module.params['list_backup_jobs_by_backup_vault_name'],
                    # TODO: make created after/before parameter work
                    # ByCreatedBefore=module.params['list_backup_jobs_by_created_before'],
                    # ByCreatedAfter=module.params['list_backup_jobs_by_created_after'],
                    ByResourceType=module.params['list_backup_jobs_by_resource_type'],
                    ByAccountId=module.params['list_backup_jobs_by_account_id']
                ), True
            else:
                return backup.list_backup_jobs(
                    ByResourceArn=module.params['list_backup_jobs_by_resource_arn'],
                    ByState=module.params['list_backup_jobs_by_state'],
                    ByBackupVaultName=module.params['list_backup_jobs_by_backup_vault_name'],
                    # TODO: make created after/before parameter work
                    # ByCreatedBefore=module.params['list_backup_jobs_by_created_before'],
                    # ByCreatedAfter=module.params['list_backup_jobs_by_created_after'],
                    ByResourceType=module.params['list_backup_jobs_by_resource_type'],
                    ByAccountId=module.params['list_backup_jobs_by_account_id']
                ), False
        elif module.params['list_copy_jobs']:
            if backup.can_paginate('list_copy_jobs'):
                paginator = backup.get_paginator('list_copy_jobs')
                return paginator.paginate(
                    ByResourceArn=module.params['list_copy_jobs_by_resource_arn'],
                    ByState=module.params['list_copy_jobs_by_state'],
                    # TODO: make created after/before parameter work
                    # ByCreatedBefore=module.params['list_backup_jobs_by_created_before'],
                    # ByCreatedAfter=module.params['list_backup_jobs_by_created_after'],
                    ByResourceType=module.params['list_copy_jobs_by_resource_type'],
                    ByAccountId=module.params['list_copy_jobs_by_account_id'],
                    ByDestinationVaultArn=module.params['list_copy_jobs_by_destination_vault_arn']
                ), True
            else:
                return backup.list_copy_jobs(
                    ByResourceArn=module.params['list_copy_jobs_by_resource_arn'],
                    ByState=module.params['list_copy_jobs_by_state'],
                    # TODO: make created after/before parameter work
                    # ByCreatedBefore=module.params['list_backup_jobs_by_created_before'],
                    # ByCreatedAfter=module.params['list_backup_jobs_by_created_after'],
                    ByResourceType=module.params['list_copy_jobs_by_resource_type'],
                    ByAccountId=module.params['list_copy_jobs_by_account_id'],
                    ByDestinationVaultArn=module.params['list_copy_jobs_by_destination_vault_arn']
                ), False
        else:
            if backup.can_paginate('list_backup_plans'):
                paginator = backup.get_paginator('list_backup_plans')
                return paginator.paginate(
                    IncludeDeleted=module.params['list_backup_plans_include_deleted']
                ), True
            else:
                return backup.list_backup_plans(
                    IncludeDeleted=module.params['list_backup_plans_include_deleted']
                ), False

    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws backup details')


def main():
    argument_spec = dict(
        backup_plan_id=dict(required=False),
        list_backup_selections=dict(required=False, type=bool, default=False),
        list_backup_plans_include_deleted=dict(required=False, type=bool, default=False),
        list_backup_plan_versions=dict(required=False, type=bool, default=False),
        list_backup_plan_templates=dict(required=False, type=bool, default=False),
        list_backup_vaults=dict(required=False, type=bool, default=False),
        # list backup jobs params
        list_backup_jobs=dict(required=False, type=bool, default=False),
        list_backup_jobs_by_resource_arn=dict(required=False, default=''),
        list_backup_jobs_by_state=dict(required=False, default=''),
        list_backup_jobs_by_backup_vault_name=dict(required=False, default=''),
        # TODO: make created after/before parameter work
        # list_backup_jobs_by_created_before=dict(required=False, default=datetime(9000, 1, 1)),
        # list_backup_jobs_by_created_after=dict(required=False, default=datetime(1000, 1, 1)),
        list_backup_jobs_by_resource_type=dict(required=False, default=''),
        list_backup_jobs_by_account_id=dict(required=False, default=''),
        # list copy jobs params
        list_copy_jobs=dict(required=False, type=bool, default=False),
        list_copy_jobs_by_resource_arn=dict(required=False, default=''),
        list_copy_jobs_by_state=dict(required=False, default=''),
        # TODO: make created after/before parameter work
        # list_copy_jobs_by_created_before=dict(required=False, default=datetime(9000, 1, 1)),
        # list_copy_jobs_by_created_after=dict(required=False, default=datetime(1000, 1, 1)),
        list_copy_jobs_by_resource_type=dict(required=False, default=''),
        list_copy_jobs_by_account_id=dict(required=False, default=''),
        list_copy_jobs_by_destination_vault_arn=dict(required=False, default=''),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_backup_selections', True, ['backup_plan_id']),
            ('list_backup_plan_versions', True, ['backup_plan_id']),
            # backup job conditions
            ('list_backup_jobs_by_resource_arn', True, ['list_backup_jobs']),
            ('list_backup_jobs_by_state', True, ['list_backup_jobs']),
            ('list_backup_jobs_by_backup_vault_name', True, ['list_backup_jobs']),
            # TODO: make created after/before parameter work
            # ('list_backup_jobs_by_created_before', True, ['list_backup_jobs']),
            # ('list_backup_jobs_by_created_after', True, ['list_backup_jobs']),
            ('list_backup_jobs_by_resource_type', True, ['list_backup_jobs']),
            ('list_backup_jobs_by_account_id', True, ['list_backup_jobs']),
            # copy jobs conditions
            ('list_copy_jobs_by_resource_arn', True, ['list_copy_jobs']),
            ('list_copy_jobs_by_state', True, ['list_copy_jobs']),
            # TODO: make created after/before parameter work
            # ('list_copy_jobs_by_created_before', True, ['list_copy_jobs']),
            # ('list_copy_jobs_by_created_after', True, ['list_copy_jobs']),
            ('list_copy_jobs_by_resource_type', True, ['list_copy_jobs']),
            ('list_copy_jobs_by_account_id', True, ['list_copy_jobs']),
            ('list_copy_jobs_by_destination_vault_arn', True, ['list_copy_jobs']),
        ),
        mutually_exclusive=[
            (
                'backup_plan_id',
                'list_backup_plans_include_deleted',
                'list_backup_plan_templates',
                'list_backup_vaults',
                'list_backup_jobs',
                'list_copy_jobs'
            ),
            (
                'list_backup_selections',
                'list_backup_plan_versions',
                'list_backup_plans_include_deleted',
                'list_backup_plan_templates',
                'list_backup_vaults',
                'list_backup_jobs',
                'list_copy_jobs'
            )
        ],
    )

    __default_return = []

    _it, _can_paginate = _backup(module)
    if _it is not None:
        if module.params['backup_plan_id'] is not None:
            if module.params['list_backup_selections']:
                if _can_paginate:
                    for response in _it:
                        for _b_plan in response['BackupSelectionsList']:
                            __default_return.append(camel_dict_to_snake_dict(_b_plan))
                else:
                    for _b_plan in _it['BackupSelectionsList']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
                module.exit_json(backup_plan_selections=__default_return)
            elif module.params['list_backup_plan_versions']:
                if _can_paginate:
                    for response in _it:
                        for _b_plan in response['BackupPlanVersionsList']:
                            __default_return.append(camel_dict_to_snake_dict(_b_plan))
                else:
                    for _b_plan in _it['BackupPlanVersionsList']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
                module.exit_json(backup_plan_versions=__default_return)
        elif module.params['list_backup_plan_templates']:
            if _can_paginate:
                for response in _it:
                    for _b_plan in response['BackupPlanTemplatesList']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
            else:
                for _b_plan in _it['BackupPlanTemplatesList']:
                    __default_return.append(camel_dict_to_snake_dict(_b_plan))
            module.exit_json(backup_plan_templates=__default_return)
        elif module.params['list_backup_vaults']:
            if _can_paginate:
                for response in _it:
                    for _b_plan in response['BackupVaultList']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
            else:
                for _b_plan in _it['BackupVaultList']:
                    __default_return.append(camel_dict_to_snake_dict(_b_plan))
            module.exit_json(backup_vaults=__default_return)
        elif module.params['list_backup_jobs']:
            if _can_paginate:
                for response in _it:
                    for _b_plan in response['BackupJobs']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
            else:
                for _b_plan in _it['BackupJobs']:
                    __default_return.append(camel_dict_to_snake_dict(_b_plan))
            module.exit_json(backup_jobs=__default_return)
        elif module.params['list_copy_jobs']:
            if _can_paginate:
                for response in _it:
                    for _b_plan in response['CopyJobs']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
            else:
                for _b_plan in _it['CopyJobs']:
                    __default_return.append(camel_dict_to_snake_dict(_b_plan))
            module.exit_json(copy_jobs=__default_return)
        else:
            if _can_paginate:
                for response in _it:
                    for _b_plan in response['BackupPlansList']:
                        __default_return.append(camel_dict_to_snake_dict(_b_plan))
            else:
                for _b_plan in _it['BackupPlansList']:
                    __default_return.append(camel_dict_to_snake_dict(_b_plan))
            module.exit_json(backup_plans=__default_return)


if __name__ == '__main__':
    main()
