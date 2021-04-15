#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_sso_admin_info
short_description: Get Information about AWS Single Sign-On Admin (SSO Admin).
description:
  - Get Information about AWS Single Sign-On Admin (SSO Admin).
  - U(https://docs.aws.amazon.com/singlesignon/latest/APIReference/API_Operations.html)
version_added: 0.0.9
options:
  instance_arn:
    description:
      - sso instance arn.
    required: false
    type: str
  account_id:
    description:
      - aws account.
    required: false
    type: str
  permission_set_arn:
    description:
      - sso permission set arn.
    required: false
    type: str
  status:
    description:
      - status to filter results.
    required: false
    type: str
    choices: ['IN_PROGRESS', 'FAILED', 'SUCCEEDED']
    default: 'IN_PROGRESS'
  list_account_assignment_creation_status:
    description:
      - do you want to get list of account_assignment_creation_status for given I(instance_arn) and I(status)?
    required: false
    type: bool
  list_account_assignment_deletion_status:
    description:
      - do you want to get account_assignment_deletion_status for given I(instance_arn) and I(status)?
    required: false
    type: bool
  list_account_assignments:
    description:
      - do you want to get list of account_assignments for given I(instance_arn), I(permission_set_arn), and I(account_id)?
    required: false
    type: bool
  list_accounts_for_provisioned_permission_set:
    description:
      - do you want to get accounts_for_provisioned_permission_set for given I(instance_arn) and I(permission_set_arn)?
    required: false
    type: bool
  list_instances:
    description:
      - do you want to get instances?
    required: false
    type: bool
  list_managed_policies_in_permission_set:
    description:
      - do you want to get managed_policies_in_permission_set for given I(instance_arn) and I(permission_set_arn)?
    required: false
    type: bool
  list_permission_set_provisioning_status:
    description:
      - do you want to get permission_set_provisioning_status for given I(instance_arn) and I(status)?
    required: false
    type: bool
  list_permission_sets:
    description:
      - do you want to get permission_sets for given I(instance_arn)?
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
- name: "get list of account_assignment_creation_status"
  aws_sso_admin_info:
    list_account_assignment_creation_status: true
    instance_arn: 'test_arn'
    status: 'IN_PROGRESS'

- name: "get account_assignment_deletion_status"
  aws_sso_admin_info:
    list_account_assignment_deletion_status: true
    instance_arn: 'test_arn'
    status: 'IN_PROGRESS'

- name: "get list of account_assignments"
  aws_sso_admin_info:
    list_account_assignments: true
    instance_arn: 'test_arn'
    permission_set_arn: 'test_arn'
    account_id: '1234567890'

- name: "get accounts_for_provisioned_permission_set"
  aws_sso_admin_info:
    list_accounts_for_provisioned_permission_set: true
    instance_arn: 'test_arn'
    permission_set_arn: 'test_arn'

- name: "get instances"
  aws_sso_admin_info:
    list_instances: true

- name: "get managed_policies_in_permission_set"
  aws_sso_admin_info:
    list_managed_policies_in_permission_set: true
    instance_arn: 'test_arn'
    permission_set_arn: 'test_arn'

- name: "get permission_set_provisioning_status"
  aws_sso_admin_info:
    list_permission_set_provisioning_status: true
    instance_arn: 'test_arn'
    status: 'IN_PROGRESS'

- name: "get permission_sets"
  aws_sso_admin_info:
    list_permission_sets: true
    instance_arn: 'test_arn'
"""

RETURN = """
account_assignment_creation_status:
  description: list of account_assignment_creation_status.
  returned: when `list_account_assignment_creation_status` is defined and success.
  type: list
account_assignment_deletion_status:
  description: list of account_assignment_deletion_status.
  returned: when `list_account_assignment_deletion_status` is defined and success.
  type: list
account_assignments:
  description: list of account_assignments.
  returned: when `list_account_assignments` is defined and success.
  type: list
accounts_for_provisioned_permission_set:
  description: list of accounts_for_provisioned_permission_set.
  returned: when `list_accounts_for_provisioned_permission_set` is defined and success.
  type: list
instances:
  description: list of instances.
  returned: when `list_instances` is defined and success.
  type: list
managed_policies_in_permission_set:
  description: list of managed_policies_in_permission_set.
  returned: when `list_managed_policies_in_permission_set` is defined and success.
  type: list
permission_set_provisioning_status:
  description: list of permission_set_provisioning_status.
  returned: when `list_permission_set_provisioning_status` is defined and success.
  type: list
permission_sets:
  description: list of permission_sets.
  returned: when `list_permission_sets` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _sso_admin(client, module):
    try:
        if module.params['list_account_assignment_creation_status']:
            if client.can_paginate('list_account_assignment_creation_status'):
                paginator = client.get_paginator('list_account_assignment_creation_status')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), True
            else:
                return client.list_account_assignment_creation_status(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), False
        elif module.params['list_account_assignment_deletion_status']:
            if client.can_paginate('list_account_assignment_deletion_status'):
                paginator = client.get_paginator('list_account_assignment_deletion_status')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), True
            else:
                return client.list_account_assignment_deletion_status(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), False
        elif module.params['list_account_assignments']:
            if client.can_paginate('list_account_assignments'):
                paginator = client.get_paginator('list_account_assignments')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    AccountId=module.params['account_id'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), True
            else:
                return client.list_account_assignments(
                    InstanceArn=module.params['instance_arn'],
                    AccountId=module.params['account_id'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), False
        elif module.params['list_accounts_for_provisioned_permission_set']:
            if client.can_paginate('list_accounts_for_provisioned_permission_set'):
                paginator = client.get_paginator('list_accounts_for_provisioned_permission_set')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), True
            else:
                return client.list_accounts_for_provisioned_permission_set(
                    InstanceArn=module.params['instance_arn'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), False
        elif module.params['list_instances']:
            if client.can_paginate('list_instances'):
                paginator = client.get_paginator('list_instances')
                return paginator.paginate(), True
            else:
                return client.list_instances(), False
        elif module.params['list_managed_policies_in_permission_set']:
            if client.can_paginate('list_managed_policies_in_permission_set'):
                paginator = client.get_paginator('list_managed_policies_in_permission_set')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), True
            else:
                return client.list_managed_policies_in_permission_set(
                    InstanceArn=module.params['instance_arn'],
                    PermissionSetArn=module.params['permission_set_arn'],
                ), False
        elif module.params['list_permission_set_provisioning_status']:
            if client.can_paginate('list_permission_set_provisioning_status'):
                paginator = client.get_paginator('list_permission_set_provisioning_status')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), True
            else:
                return client.list_permission_set_provisioning_status(
                    InstanceArn=module.params['instance_arn'],
                    Filter={
                        'Status': module.params['status']
                    }
                ), False
        elif module.params['list_permission_sets']:
            if client.can_paginate('list_permission_sets'):
                paginator = client.get_paginator('list_permission_sets')
                return paginator.paginate(
                    InstanceArn=module.params['instance_arn'],
                ), True
            else:
                return client.list_permission_sets(
                    InstanceArn=module.params['instance_arn'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch AWS Single Sign-On Admin (SSO Admin) details')


def main():
    argument_spec = dict(
        instance_arn=dict(required=False),
        account_id=dict(required=False),
        permission_set_arn=dict(required=False),
        status=dict(
            required=False,
            choices=['IN_PROGRESS', 'FAILED', 'SUCCEEDED'],
            default='IN_PROGRESS'
        ),
        list_account_assignment_creation_status=dict(required=False, type=bool),
        list_account_assignment_deletion_status=dict(required=False, type=bool),
        list_account_assignments=dict(required=False, type=bool),
        list_accounts_for_provisioned_permission_set=dict(required=False, type=bool),
        list_instances=dict(required=False, type=bool),
        list_managed_policies_in_permission_set=dict(required=False, type=bool),
        list_permission_set_provisioning_status=dict(required=False, type=bool),
        list_permission_sets=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_account_assignment_creation_status', True, ['instance_arn']),
            ('list_account_assignment_deletion_status', True, ['instance_arn']),
            ('list_account_assignments', True, ['instance_arn', 'account_id', 'permission_set_arn']),
            ('list_accounts_for_provisioned_permission_set', True, ['instance_arn', 'permission_set_arn']),
            ('list_managed_policies_in_permission_set', True, ['instance_arn', 'permission_set_arn']),
            ('list_permission_set_provisioning_status', True, ['instance_arn']),
            ('list_permission_sets', True, ['instance_arn']),
        ),
        mutually_exclusive=[
            (
                'list_account_assignment_creation_status',
                'list_account_assignment_deletion_status',
                'list_account_assignments',
                'list_accounts_for_provisioned_permission_set',
                'list_instances',
                'list_managed_policies_in_permission_set',
                'list_permission_set_provisioning_status',
                'list_permission_sets',
            )
        ],
    )

    client = module.client('sso-admin', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _sso_admin(client, module)

    if module.params['list_account_assignment_creation_status']:
        module.exit_json(account_assignment_creation_status=aws_response_list_parser(paginate, it, 'AccountAssignmentsCreationStatus'))
    elif module.params['list_account_assignment_deletion_status']:
        module.exit_json(account_assignment_deletion_status=aws_response_list_parser(paginate, it, 'AccountAssignmentsDeletionStatus'))
    elif module.params['list_account_assignments']:
        module.exit_json(account_assignments=aws_response_list_parser(paginate, it, 'AccountAssignments'))
    elif module.params['list_accounts_for_provisioned_permission_set']:
        module.exit_json(accounts_for_provisioned_permission_set=aws_response_list_parser(paginate, it, 'AccountIds'))
    elif module.params['list_instances']:
        module.exit_json(instances=aws_response_list_parser(paginate, it, 'Instances'))
    elif module.params['list_managed_policies_in_permission_set']:
        module.exit_json(managed_policies_in_permission_set=aws_response_list_parser(paginate, it, 'AttachedManagedPolicies'))
    elif module.params['list_permission_set_provisioning_status']:
        module.exit_json(permission_set_provisioning_status=aws_response_list_parser(paginate, it, 'PermissionSetsProvisioningStatus'))
    elif module.params['list_permission_sets']:
        module.exit_json(permission_sets=aws_response_list_parser(paginate, it, 'PermissionSets'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
