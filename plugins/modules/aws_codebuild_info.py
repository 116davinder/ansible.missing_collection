#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codebuild_info
short_description: Get Information about AWS Code Build.
description:
  - Get Information about AWS Code Build.
  - U(https://docs.aws.amazon.com/codebuild/latest/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  project_names:
    description:
      - list of the project names or arns?
    required: false
    type: list
  project_name:
    description:
      - name of the project.
    required: false
    type: str
  report_group_arn:
    description:
      - arn of report group.
    required: false
    type: str
  sort_by:
    description:
      - filter to sort the results.
      - check AWS API Documentation for different options.
    required: false
    type: str
  sort_order:
    description:
      - In which order you want to sort your results.
    required: false
    type: str
    choices: ['ASCENDING', 'DESCENDING']
    default: 'ASCENDING'
  report_filter_status:
    description:
      - what is the status of the report?
    required: false
    type: str
    choices: ['GENERATING', 'SUCCEEDED', 'FAILED', 'INCOMPLETE', 'DELETING']
    default: 'SUCCEEDED'
  list_projects:
    description:
      - do you want to get list of all projects for given I(order_by) and I(sort_order)?
    required: false
    type: bool
  list_shared_projects:
    description:
      - do you want to get list of all shared projects for given I(order_by) and I(sort_order)?
    required: false
    type: bool
  list_report_groups:
    description:
      - do you want to get list of all report groups for given I(order_by) and I(sort_order)?
    required: false
    type: bool
  list_shared_report_groups:
    description:
      - do you want to get list of all shared report groups for given I(order_by) and I(sort_order)?
    required: false
    type: bool
  list_reports:
    description:
      - do you want to get list of all reports for given I(report_filter_status) and I(sort_order)?
    required: false
    type: bool
  list_reports_for_report_group:
    description:
      - do you want to get list of all reports for given I(report_group_arn), I(report_filter_status) and I(sort_order)?
    required: false
    type: bool
  list_builds:
    description:
      - do you want to get list of all builds for given I(sort_order)?
    required: false
    type: bool
  list_builds_for_project:
    description:
      - do you want to get list of all builds for given I(project_name) and I(sort_order)?
    required: false
    type: bool
  describe_projects:
    description:
      - do you want to get description of given I(project_names)?
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
- name: "get list of all projects"
  aws_codebuild_info:
    list_projects: true
    sort_by: 'NAME'
    sort_order: 'ASCENDING'

- name: "get list of all shared projects"
  aws_codebuild_info:
    list_shared_projects: true
    sort_by: 'ARN'
    sort_order: 'ASCENDING'

- name: "get list of all report groups"
  aws_codebuild_info:
    list_report_groups: true
    sort_by: 'NAME'
    sort_order: 'ASCENDING'

- name: "get list of all shared report groups"
  aws_codebuild_info:
    list_shared_report_groups: true
    sort_by: 'ARN'
    sort_order: 'ASCENDING'

- name: "get list of all reports"
  aws_codebuild_info:
    list_reports: true
    report_filter_status: 'SUCCEEDED'
    sort_order: 'ASCENDING'

- name: "get list of all reports for given report_group"
  aws_codebuild_info:
    list_reports_for_report_group: true
    report_filter_status: 'SUCCEEDED'
    sort_order: 'ASCENDING'
    report_group_arn: 'aws:::test'

- name: "get list of all builds"
  aws_codebuild_info:
    list_builds: true
    sort_order: 'ASCENDING'

- name: "get list of all builds for given project"
  aws_codebuild_info:
    list_builds_for_project: true
    project_name: 'test'
    sort_order: 'ASCENDING'

- name: "get details about given project names or arns"
  aws_codebuild_info:
    describe_projects: true
    project_names: ['test']
"""

RETURN = """
project_ids:
  description: list of all projects or shared projects.
  returned: when (`list_projects`, `sort_order`, and `sort_by`) or (`list_shared_projects`, `sort_by`, and `sort_order`) are defined and success
  type: list
  sample: ['string',]
report_group_ids:
  description: list of all report groups or shared report groups.
  returned: when (`list_report_groups`, `sort_order`, and `sort_by`) or (`list_shared_report_groups`, `sort_by`, and `sort_order`) are defined and success
  type: list
  sample: ['string',]
report_arns:
  description: list of all report or project specific report arns.
  returned: when (`list_reports`, `sort_order`, and `report_filter_status`) or (`list_reports_for_report_group`, `report_group_arn`, `sort_order`, and `report_filter_status`) are defined and success
  type: list
  sample: ['string',]
build_ids:
  description: list of all build ids or project specific build ids.
  returned: when (`list_builds`, and `sort_order`) or (`list_builds_for_project`, `project_name`, and `sort_order`) are defined and success
  type: list
  sample: ['string',]
projects:
  description: description of all given project names.
  returned: when `describe_projects`, and `project_names` are defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'arn': 'string',
        'description': 'string',
        'source': {},
        'secondary_sources': [],
        'source_version': 'string',
        'secondary_Source_versions': [],
        'artifacts': {},
        'secondary_artifacts': [],
        'cache': {},
        'environment': {},
        'service_role': 'string',
        'timeout_in_minutes': 123,
        'queued_timeout_in_minutes': 123,
        'encryption_key': 'string',
        'tags': [],
        'created': datetime(2016, 6, 6),
        'last_modified': datetime(2015, 1, 1),
        'webhook': {},
        'vpc_config': {},
        'badge': {},
        'logs_config': {},
        'file_system_locations': [],
        'build_batch_config': {}
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
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator[resource_field]:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _codebuild(client, module):
    try:
        if module.params['list_projects']:
            if client.can_paginate('list_projects'):
                paginator = client.get_paginator('list_projects')
                return paginator.paginate(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_projects(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_shared_projects']:
            if client.can_paginate('list_shared_projects'):
                paginator = client.get_paginator('list_shared_projects')
                return paginator.paginate(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_shared_projects(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_report_groups']:
            if client.can_paginate('list_report_groups'):
                paginator = client.get_paginator('list_report_groups')
                return paginator.paginate(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_report_groups(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_shared_report_groups']:
            if client.can_paginate('list_shared_report_groups'):
                paginator = client.get_paginator('list_shared_report_groups')
                return paginator.paginate(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_shared_report_groups(
                    sortBy=module.params['sort_by'],
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_reports']:
            if client.can_paginate('list_reports'):
                paginator = client.get_paginator('list_reports')
                return paginator.paginate(
                    filter={
                        'status': module.params['report_filter_status']
                    },
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_reports(
                    filter={
                        'status': module.params['report_filter_status']
                    },
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_reports_for_report_group']:
            if client.can_paginate('list_reports_for_report_group'):
                paginator = client.get_paginator('list_reports_for_report_group')
                return paginator.paginate(
                    reportGroupArn=module.params['report_group_arn'],
                    filter={
                        'status': module.params['report_filter_status']
                    },
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_reports_for_report_group(
                    reportGroupArn=module.params['report_group_arn'],
                    filter={
                        'status': module.params['report_filter_status']
                    },
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_builds']:
            if client.can_paginate('list_builds'):
                paginator = client.get_paginator('list_builds')
                return paginator.paginate(
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_builds(
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['list_builds_for_project']:
            if client.can_paginate('list_builds_for_project'):
                paginator = client.get_paginator('list_builds_for_project')
                return paginator.paginate(
                    projectName=module.params['project_name'],
                    sortOrder=module.params['sort_order']
                ), True
            else:
                return client.list_builds_for_project(
                    projectName=module.params['project_name'],
                    sortOrder=module.params['sort_order']
                ), False
        elif module.params['describe_projects']:
            if client.can_paginate('batch_get_projects'):
                paginator = client.get_paginator('batch_get_projects')
                return paginator.paginate(
                    names=module.params['project_names'],
                ), True
            else:
                return client.batch_get_projects(
                    names=module.params['project_names'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws code build details')


def main():
    argument_spec = dict(
        project_names=dict(required=False, type=list),
        project_name=dict(required=False),
        report_group_arn=dict(required=False),
        sort_by=dict(required=False),
        sort_order=dict(required=False, choices=['ASCENDING', 'DESCENDING'], default='ASCENDING'),
        report_filter_status=dict(required=False, choices=['GENERATING', 'SUCCEEDED', 'FAILED', 'INCOMPLETE', 'DELETING'], default='SUCCEEDED'),
        list_projects=dict(required=False, type=bool),
        list_shared_projects=dict(required=False, type=bool),
        list_report_groups=dict(required=False, type=bool),
        list_shared_report_groups=dict(required=False, type=bool),
        list_reports=dict(required=False, type=bool),
        list_reports_for_report_group=dict(required=False, type=bool),
        list_builds=dict(required=False, type=bool),
        list_builds_for_project=dict(required=False, type=bool),
        describe_projects=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_projects', True, ['sort_by']),
            ('list_shared_projects', True, ['sort_by']),
            ('list_report_groups', True, ['sort_by']),
            ('list_shared_report_groups', True, ['sort_by']),
            ('list_reports_for_report_group', True, ['report_group_arn']),
            ('list_builds_for_project', True, ['project_name']),
            ('describe_projects', True, ['project_names']),
        ),
        mutually_exclusive=[
            (
                'list_projects',
                'list_shared_projects',
                'list_report_groups',
                'list_shared_report_groups',
                'list_reports',
                'list_reports_for_report_group',
                'list_builds',
                'list_builds_for_project',
                'describe_projects',
            )
        ],
    )

    client = module.client('codebuild', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codebuild(client, module)

    if module.params['list_projects'] or module.params['list_shared_projects']:
        module.exit_json(project_ids=aws_response_list_parser(paginate, _it, 'projects'))
    elif module.params['list_report_groups'] or module.params['list_shared_report_groups']:
        module.exit_json(report_group_ids=aws_response_list_parser(paginate, _it, 'reportGroups'))
    elif module.params['list_reports'] or module.params['list_reports_for_report_group']:
        module.exit_json(report_arns=aws_response_list_parser(paginate, _it, 'reports'))
    elif module.params['list_builds'] or module.params['list_builds_for_project']:
        module.exit_json(build_ids=aws_response_list_parser(paginate, _it, 'ids'))
    elif module.params['describe_projects']:
        module.exit_json(projects=aws_response_list_parser(paginate, _it, 'projects'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
