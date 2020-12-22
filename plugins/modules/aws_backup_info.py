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
version_added: 1.4.0
options:
  name:
    description:
      - name of the athena catalog.
      - Mutually Exclusive: I(list_work_groups) and I(name).
    required: false
    type: str
    aliases: ['catalog_name']
  database_name:
    description:
      - name of the athena database.
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
"""

RETURN = """
catalogs:
  description: List of Athena Catalogs.
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        "catalog_name": "AwsDataCatalog",
        "type": "GLUE"
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
        list_backup_selections=dict(required=False, type=bool),
        list_backup_plans_include_deleted=dict(required=False, type=bool, default=False),
        list_backup_plan_versions=dict(required=False, type=bool),
        list_backup_plan_templates=dict(required=False, type=bool),
        list_backup_vaults=dict(required=False, type=bool)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_backup_selections', True, ['backup_plan_id']),
            ('list_backup_plan_versions', True, ['backup_plan_id']),
        ),
        mutually_exclusive=[
            ('backup_plan_id', 'list_backup_plans_include_deleted'),
            (
                'list_backup_selections',
                'list_backup_plans_include_deleted',
                'list_backup_plan_versions',
                'list_backup_plan_templates',
                'list_backup_vaults'
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
