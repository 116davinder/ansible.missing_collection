#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_auditmanager_info
short_description: Get details about AWS Audit Manager.
description:
  - Get Information about AWS Audit Manager.
  - U(https://docs.aws.amazon.com/audit-manager/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  name:
    description:
      - name of resource group.
    required: false
    type: str
    aliases: ['resource_group_name']
  list_components:
    description:
      - do you want to fetch all components of given group name I(name)?
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
- name: "list of all assessments from AWS Audit Manager"
  aws_auditmanager_info:

- name: "list of all AWS Audit Manager framework library"
  aws_auditmanager_info:
    type: 'Standard'
    list_assessment_frameworks: true

- name: "list of assessment reports created in AWS Audit Manager"
  aws_auditmanager_info:
    list_assessment_reports: true

- name: "list of controls from AWS Audit Manager"
  aws_auditmanager_info:
    type: 'Standard'
    list_controls: true

- name: "list of all AWS Audit Manager notifications"
  aws_auditmanager_info:
    list_notifications: true

- name: "list of delegations from an audit owner to a delegate"
  aws_auditmanager_info:
    list_delegations: true
"""

RETURN = """
assessments:
  description: Returns a list of current and past assessments from AWS Audit Manager.
  returned: when no argument and success
  type: list
  sample: [
      {
          'name': 'string',
          'id': 'string',
          'compliance_type': 'string',
          'status': 'ACTIVE',
          'roles': [
              {
                  'role_type': 'PROCESS_OWNER',
                  'role_arn': 'string'
              },
          ],
          'delegations': [
              {
                  'id': 'string',
                  'assessment_name': 'string',
                  'assessment_id': 'string',
                  'status': 'IN_PROGRESS',
                  'role_arn': 'string',
                  'role_type': 'PROCESS_OWNER',
                  'creation_time': datetime(2017, 7, 7),
                  'last_updated': datetime(2016, 6, 6),
                  'control_set_id': 'string',
                  'comment': 'string',
                  'created_by': 'string'
              },
          ],
          'creation_time': datetime(2018, 8, 8),
          'last_updated': datetime(2015, 1, 1)
      },
  ]
framework_metadata_list:
  description: Returns a list of the frameworks available in the AWS Audit Manager framework library.
  returned: when `list_assessment_frameworks` and `type` are defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'type': 'Standard',
          'name': 'string',
          'description': 'string',
          'logo': 'string',
          'compliance_type': 'string',
          'controls_count': 123,
          'control_sets_count': 123,
          'created_at': datetime(2016, 6, 6),
          'last_updated_at': datetime(2015, 1, 1)
      },
  ]
assessment_reports:
  description: Returns a list of assessment reports created in AWS Audit Manager.
  returned: when `list_assessment_reports` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'name': 'string',
          'description': 'string',
          'assessment_id': 'string',
          'assessment_name': 'string',
          'author': 'string',
          'status': 'COMPLETE',
          'creation_time': datetime(2015, 1, 1)
      },
  ]
control_metadata_list:
  description: Returns a list of controls from AWS Audit Manager.
  returned: when `list_controls` and `type` are defined and success
  type: list
  sample: [
      {
          'arn': 'string',
          'id': 'string',
          'name': 'string',
          'control_sources': 'string',
          'created_at': datetime(2016, 6, 6),
          'last_updated_at': datetime(2015, 1, 1)
      },
  ]
notifications:
  description: Returns a list of all AWS Audit Manager notifications.
  returned: when `list_notifications` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'assessment_id': 'string',
          'assessment_name': 'string',
          'control_set_id': 'string',
          'control_set_name': 'string',
          'description': 'string',
          'event_time': datetime(2015, 1, 1),
          'source': 'string'
      },
  ]
delegations:
  description: Returns a list of delegations from an audit owner to a delegate.
  returned: when `list_delegations` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'assessment_name': 'string',
          'assessment_id': 'string',
          'status': 'IN_PROGRESS',
          'role_arn': 'string',
          'creation_time': datetime(2015, 1, 1),
          'control_set_name': 'string'
      },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _auditmanager(client, module):
    try:
        if module.params['list_assessment_frameworks']:
            if client.can_paginate('list_assessment_frameworks'):
                paginator = client.get_paginator('list_assessment_frameworks')
                return paginator.paginate(
                    frameworkType=module.params['type']
                ), True
            else:
                return client.list_assessment_frameworks(
                    frameworkType=module.params['type']
                ), False
        elif module.params['list_assessment_reports']:
            if client.can_paginate('list_assessment_reports'):
                paginator = client.get_paginator('list_assessment_reports')
                return paginator.paginate(), True
            else:
                return client.list_assessment_reports(), False
        elif module.params['list_controls']:
            if client.can_paginate('list_controls'):
                paginator = client.get_paginator('list_controls')
                return paginator.paginate(
                    controlType=module.params['type']
                ), True
            else:
                return client.list_controls(
                    controlType=module.params['type']
                ), False
        elif module.params['list_notifications']:
            if client.can_paginate('list_notifications'):
                paginator = client.get_paginator('list_notifications')
                return paginator.paginate(), True
            else:
                return client.list_notifications(), False
        elif module.params['list_delegations']:
            if client.can_paginate('get_delegations'):
                paginator = client.get_paginator('get_delegations')
                return paginator.paginate(), True
            else:
                return client.get_delegations(), False
        else:
            if client.can_paginate('list_assessments'):
                paginator = client.get_paginator('list_assessments')
                return paginator.paginate(), True
            else:
                return client.list_assessments(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws audit manager details')


def main():
    argument_spec = dict(
        type=dict(required=False, choices=['Standard', 'Custom']),
        list_assessment_frameworks=dict(required=False, type=bool),
        list_assessment_reports=dict(required=False, type=bool),
        list_controls=dict(required=False, type=bool),
        list_notifications=dict(required=False, type=bool),
        list_delegations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_assessment_frameworks', True, ['type']),
            ('list_controls', True, ['type']),
        ],
        mutually_exclusive=[
            (
                'list_assessment_frameworks',
                'list_assessment_reports',
                'list_controls',
                'list_notifications',
                'list_delegations',
            ),
        ],
    )

    client = module.client('auditmanager', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _auditmanager(client, module)

    if module.params['list_assessment_frameworks']:
        module.exit_json(framework_metadata_list=aws_response_list_parser(paginate, _it, 'frameworkMetadataList'))
    elif module.params['list_assessment_reports']:
        module.exit_json(assessment_reports=aws_response_list_parser(paginate, _it, 'assessmentReports'))
    elif module.params['list_controls']:
        module.exit_json(control_metadata_list=aws_response_list_parser(paginate, _it, 'controlMetadataList'))
    elif module.params['list_notifications']:
        module.exit_json(notifications=aws_response_list_parser(paginate, _it, 'notifications'))
    elif module.params['list_delegations']:
        module.exit_json(delegations=aws_response_list_parser(paginate, _it, 'delegations'))
    else:
        module.exit_json(assessments=aws_response_list_parser(paginate, _it, 'assessmentMetadata'))


if __name__ == '__main__':
    main()
