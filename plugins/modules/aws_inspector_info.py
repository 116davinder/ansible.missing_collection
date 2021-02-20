#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_inspector_info
short_description: Get Information about Amazon Inspector.
description:
  - Get Information about Amazon Inspector.
  - U(https://docs.aws.amazon.com/inspector/latest/APIReference/API_Operations.html)
version_added: 0.0.7
options:
  arn:
    description:
      - can be arn of assessment run?
    required: false
    type: str
    aliases: ['assessment_run_arn']
  arns:
    description:
      - can be list of assessment_template_arns?
      - can be list of assessment_target_arns?
      - can be list of assessment_run_arns?
    required: false
    type: list
    aliases: ['assessment_template_arns', 'assessment_target_arns', 'assessment_run_arns']
    default: []
  list_assessment_run_agents:
    description:
      - do you want to get list of assessment_run_agents for given assessment I(arn)?
    required: false
    type: bool
  list_assessment_runs:
    description:
      - do you want to get list of assessment_runs for given template I(arns)?
    required: false
    type: bool
  list_assessment_targets:
    description:
      - do you want to get list of assessment_targets?
    required: false
    type: bool
  list_assessment_templates:
    description:
      - do you want to get list of assessment_templates for given assessment I(arns)?
    required: false
    type: bool
  list_event_subscriptions:
    description:
      - do you want to get list of event_subscriptions?
    required: false
    type: bool
  list_exclusions:
    description:
      - do you want to get list of exclusions for given assessment I(arn)?
    required: false
    type: bool
  list_findings:
    description:
      - do you want to get list of findings for given assessment runs I(arns)?
    required: false
    type: bool
  list_rules_packages:
    description:
      - do you want to get list of rules_packages?
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
- name: "get list of assessment run agents"
  aws_inspector_info:
    list_assessment_run_agents: true
    arn: 'assessment_run_arn'

- name: "get list of assessment_runs"
  aws_inspector_info:
    list_assessment_runs: true
    arns: []

- name: "get list of assessment_targets"
  aws_inspector_info:
    list_assessment_targets: true

- name: "get list of assessment_templates"
  aws_inspector_info:
    list_assessment_templates: true
    arns: []

- name: "get list of event_subscriptions"
  aws_inspector_info:
    list_event_subscriptions: true

- name: "get list of exclusions"
  aws_inspector_info:
    list_exclusions: true
    arn: 'assessment-run-arn'

- name: "get list of findings"
  aws_inspector_info:
    list_findings: true
    arns: []

- name: "get list of rules_packages"
  aws_inspector_info:
    list_rules_packages: true
"""

RETURN = """
assessment_run_agents:
  description: list of assessment_run_agents.
  returned: when `list_assessment_run_agents` is defined and success.
  type: list
assessment_runs:
  description: list of assessment_runs.
  returned: when `list_assessment_runs` is defined and success.
  type: list
assessment_targets:
  description: list of assessment_targets.
  returned: when `list_assessment_targets` is defined and success.
  type: list
assessment_templates:
  description: list of assessment_templates.
  returned: when `list_assessment_templates` is defined and success.
  type: list
event_subscriptions:
  description: list of event_subscriptions.
  returned: when `list_event_subscriptions` is defined and success.
  type: list
exclusions:
  description: list of exclusions.
  returned: when `list_exclusions` is defined and success.
  type: list
findings:
  description: list of findings.
  returned: when `list_findings` is defined and success.
  type: list
rules_packages:
  description: list of rules_packages.
  returned: when `list_rules_packages` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _inspector(client, module):
    try:
        if module.params['list_assessment_run_agents']:
            if client.can_paginate('list_assessment_run_agents'):
                paginator = client.get_paginator('list_assessment_run_agents')
                return paginator.paginate(
                    assessmentRunArn=module.params['arn']
                ), True
            else:
                return client.list_assessment_run_agents(
                    assessmentRunArn=module.params['arn']
                ), False
        elif module.params['list_assessment_runs']:
            if client.can_paginate('list_assessment_runs'):
                paginator = client.get_paginator('list_assessment_runs')
                return paginator.paginate(
                    assessmentTemplateArns=module.params['arns']
                ), True
            else:
                return client.list_assessment_runs(
                    assessmentTemplateArns=module.params['arns']
                ), False
        elif module.params['list_assessment_targets']:
            if client.can_paginate('list_assessment_targets'):
                paginator = client.get_paginator('list_assessment_targets')
                return paginator.paginate(), True
            else:
                return client.list_assessment_targets(), False
        elif module.params['list_assessment_templates']:
            if client.can_paginate('list_assessment_templates'):
                paginator = client.get_paginator('list_assessment_templates')
                return paginator.paginate(
                    assessmentTargetArns=module.params['arns']
                ), True
            else:
                return client.list_assessment_templates(
                    assessmentTargetArns=module.params['arns']
                ), False
        elif module.params['list_event_subscriptions']:
            if client.can_paginate('list_event_subscriptions'):
                paginator = client.get_paginator('list_event_subscriptions')
                return paginator.paginate(), True
            else:
                return client.list_event_subscriptions(), False
        elif module.params['list_exclusions']:
            if client.can_paginate('list_exclusions'):
                paginator = client.get_paginator('list_exclusions')
                return paginator.paginate(
                    assessmentRunArn=module.params['arn']
                ), True
            else:
                return client.list_exclusions(
                    assessmentRunArn=module.params['arn']
                ), False
        elif module.params['list_findings']:
            if client.can_paginate('list_findings'):
                paginator = client.get_paginator('list_findings')
                return paginator.paginate(
                    assessmentRunArns=module.params['arns']
                ), True
            else:
                return client.list_findings(
                    assessmentRunArns=module.params['arns']
                ), False
        elif module.params['list_rules_packages']:
            if client.can_paginate('list_rules_packages'):
                paginator = client.get_paginator('list_rules_packages')
                return paginator.paginate(), True
            else:
                return client.list_rules_packages(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Inspector details')


def main():
    argument_spec = dict(
        arn=dict(required=False, aliases=['assessment_run_arn']),
        arns=dict(required=False, type=list, aliases=['assessment_template_arns', 'assessment_target_arns', 'assessment_run_arns'], default=[]),
        list_assessment_run_agents=dict(required=False, type=bool),
        list_assessment_runs=dict(required=False, type=bool),
        list_assessment_targets=dict(required=False, type=bool),
        list_assessment_templates=dict(required=False, type=bool),
        list_event_subscriptions=dict(required=False, type=bool),
        list_exclusions=dict(required=False, type=bool),
        list_findings=dict(required=False, type=bool),
        list_rules_packages=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_assessment_run_agents', True, ['arn']),
            ('list_assessment_runs', True, ['arns']),
            ('list_assessment_templates', True, ['arns']),
            ('list_exclusions', True, ['arn']),
            ('list_findings', True, ['arns']),
        ),
        mutually_exclusive=[
            (
                'list_assessment_run_agents',
                'list_assessment_runs',
                'list_assessment_targets',
                'list_assessment_templates',
                'list_event_subscriptions',
                'list_exclusions',
                'list_findings',
                'list_rules_packages',
            )
        ],
    )

    client = module.client('inspector', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _inspector(client, module)

    if module.params['list_assessment_run_agents']:
        module.exit_json(assessment_run_agents=aws_response_list_parser(paginate, it, 'assessmentRunAgents'))
    elif module.params['list_assessment_runs']:
        module.exit_json(assessment_runs=aws_response_list_parser(paginate, it, 'assessmentRunArns'))
    elif module.params['list_assessment_targets']:
        module.exit_json(assessment_targets=aws_response_list_parser(paginate, it, 'assessmentTargetArns'))
    elif module.params['list_assessment_templates']:
        module.exit_json(assessment_templates=aws_response_list_parser(paginate, it, 'assessmentTemplateArns'))
    elif module.params['list_event_subscriptions']:
        module.exit_json(event_subscriptions=aws_response_list_parser(paginate, it, 'subscriptions'))
    elif module.params['list_exclusions']:
        module.exit_json(exclusions=aws_response_list_parser(paginate, it, 'exclusionArns'))
    elif module.params['list_findings']:
        module.exit_json(findings=aws_response_list_parser(paginate, it, 'findingArns'))
    elif module.params['list_rules_packages']:
        module.exit_json(rules_packages=aws_response_list_parser(paginate, it, 'rulesPackageArns'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
