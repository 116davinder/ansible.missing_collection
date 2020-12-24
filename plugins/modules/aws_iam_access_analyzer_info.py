#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_iam_access_analyzer_info
short_description: Get Information about AWS IAM Access Analyzer.
description:
  - Get Information about AWS IAM Access Analyzer Resources.
  - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_Operations.html)
version_added: 1.4.0
options:
  name:
    description:
      - name of the analyzer?
    required: false
    type: str
    aliases: ['analyzer_name']
  arn:
    description:
      - arn of the analyzer?
    required: false
    type: str
    aliases: ['analyzer_arn']
  list_analyzers:
    description:
      - do you want to fetch all analyzer?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAnalyzers.html)
    required: false
    type: bool
  list_analyzers_type:
    description:
      - which type of analyzer?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAnalyzers.html)
    required: false
    choices: ['ACCOUNT', 'ORGANIZATION']
    type: str
  list_archive_rules:
    description:
      - do you want to fetch all analyzer archive rules?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListArchiveRules.html)
    required: false
    type: bool
  list_findings:
    description:
      - do you want to fetch all analyzer findings?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListFindings.html)
    required: false
    type: bool
  list_analyzed_resources:
    description:
      - do you want to fetch all analyzed resources?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAnalyzedResources.html)
    required: false
    type: bool
  list_analyzed_resources_type:
    description:
      - do you want to fetch all analyzed resources?
      - U(https://docs.aws.amazon.com/access-analyzer/latest/APIReference/API_ListAnalyzedResources.html)
    required: false
    type: str
    choices: [
        'AWS::S3::Bucket',
        'AWS::IAM::Role',
        'AWS::SQS::Queue',
        'AWS::Lambda::Function',
        'AWS::Lambda::LayerVersion',
        'AWS::KMS::Key'
    ]
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
- name: "get list of aws iam analyzers"
  aws_iam_access_analyzer_info:
    list_analyzers: true
    list_analyzers_type: 'ACCOUNT'
  register: __iam_analyzer

- name: "get list of archive rules"
  aws_iam_access_analyzer_info:
    name: "{{ __iam_analyzer.analyzers[0].name }}"
    list_archive_rules: true

- name: "get list of findings"
  aws_iam_access_analyzer_info:
    arn: "{{ __iam_analyzer.analyzers[0].arn }}"
    list_findings: true

- name: "get list of analyzed resources"
  aws_iam_access_analyzer_info:
    arn: "{{ __iam_analyzer.analyzers[0].arn }}"
    list_analyzed_resources: true
    list_analyzed_resources_type: 'AWS::S3::Bucket'
"""

RETURN = """
analyzers:
  description: List of analyzers from aws iam.
  returned: when I(list_analyzers) and I(list_analyzers_type) is defined and success
  type: list
  sample: [
    {
        "arn": "arn:aws:access-analyzer:us-east-1:xxxx:analyzer/ConsoleAnalyzer-xxxx-a0c3-2bcc56294763",
        "created_at": "2019-12-03T11:55:24+00:00",
        "last_resource_analyzed": "arn:aws:kms:us-east-1:xxxx:key/xxxxx-9c87-f17c48283fe7",
        "last_resource_analyzed_at": "2020-12-24T10:06:50.125000+00:00",
        "name": "ConsoleAnalyzer-xxxx-a0c3-2bcc56294763",
        "status": "ACTIVE",
        "tags": {},
        "type": "ACCOUNT"
    }
  ]
archive_rules:
  description: List of archive rules for given analyzer name.
  returned: when I(list_archive_rules) and I(name) is defined and success
  type: list
  sample: [
    {
        "created_at": "2020-12-24T10:20:44+00:00",
        "filter": {
            "is_public": {
                "eq": ["false"]
            }
        },
        "rule_name": "ArchiveRule-xxxxx-9d7d-c25e98a9b12f",
        "updated_at": "2020-12-24T10:20:44+00:00"
    }
  ]
findings:
  description: List of findings for given analyzer arn.
  returned: when I(list_findings) and I(arn) is defined and success
  type: list
  sample: [
    {
      "action": [
        "sts:AssumeRole"
      ],
      "analyzed_at": "2020-12-23T23:33:51.497000+00:00",
      "condition": {},
      "created_at": "2019-12-03T11:55:26+00:00",
      "id": "xxxxxxxxx-adca-d617574e694c",
      "is_public": false,
      "principal": {
        "aws": "xxxxxx"
      },
      "resource": "arn:aws:iam::xxxxxxxxxx:role/Test-Integrations",
      "resource_owner_account": "xxxxxxxxx",
      "resource_type": "AWS::IAM::Role",
      "status": "ACTIVE",
      "updated_at": "2019-12-03T11:55:26+00:00"
    }
  ]
analyzed_resources:
  description: List of analyzed resources for given analyzer arn.
  returned: when I(list_analyzed_resources) and I(list_analyzed_resources_type) and I(arn) is defined and success
  type: list
  sample: [
    {
        "resource_arn": "arn:aws:s3:::test-s3-bucket",
        "resource_owner_account": "xxxxxxxx",
        "resource_type": "AWS::S3::Bucket"
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


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if paginate:
        for response in iterator:
            for _app in response[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    else:
        for _app in iterator:
            _return.append(camel_dict_to_snake_dict(_app))
    return _return


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _iam_access_analyzer(client, module):
    try:
        if module.params['list_analyzers']:
            if client.can_paginate('list_analyzers'):
                paginator = client.get_paginator('list_analyzers')
                iterator = paginator.paginate(
                    type=module.params['list_analyzers_type']
                )
                return iterator, True
            else:
                return client.list_analyzers(
                    type=module.params['list_analyzers_type']
                ), False
        elif module.params['list_archive_rules']:
            if client.can_paginate('list_archive_rules'):
                paginator = client.get_paginator('list_archive_rules')
                return paginator.paginate(
                    analyzerName=module.params['name']
                ), True
            else:
                return client.list_archive_rules(
                    analyzerName=module.params['name']
                ), False
        elif module.params['list_findings']:
            if client.can_paginate('list_findings'):
                paginator = client.get_paginator('list_findings')
                return paginator.paginate(
                    analyzerArn=module.params['arn']
                ), True
            else:
                return client.list_findings(
                    analyzerArn=module.params['arn'],
                ), False
        elif module.params['list_analyzed_resources']:
            if client.can_paginate('list_analyzed_resources'):
                paginator = client.get_paginator('list_analyzed_resources')
                return paginator.paginate(
                    analyzerArn=module.params['arn'],
                    resourceType=module.params['list_analyzed_resources_type']
                ), True
            else:
                return client.list_analyzed_resources(
                    analyzerArn=module.params['arn'],
                    resourceType=module.params['list_analyzed_resources_type']
                ), False
        else:
            module.fail_json(msg='please pass correct arguments')
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws iam access analyzer details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['analyzer_name']),
        arn=dict(required=False, aliases=['analyzer_arn']),
        list_analyzers=dict(required=False, type=bool),
        list_analyzers_type=dict(required=False, choices=['ACCOUNT', 'ORGANIZATION']),
        list_archive_rules=dict(required=False, type=bool),
        list_findings=dict(required=False, type=bool),
        list_analyzed_resources=dict(required=False, type=bool),
        list_analyzed_resources_type=dict(
            required=False,
            choices=[
                'AWS::S3::Bucket',
                'AWS::IAM::Role',
                'AWS::SQS::Queue',
                'AWS::Lambda::Function',
                'AWS::Lambda::LayerVersion',
                'AWS::KMS::Key'
            ]
        )
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_analyzer_type', True, ['list_analyzer']),
            ('list_archive_rules', True, ['name']),
            ('list_findings', True, ['arn']),
            ('list_analyzed_resources', True, ['list_analyzed_resources_type'])
        ),
        mutually_exclusive=[
            (
                'list_analyzer_type',
                'list_archive_rules',
                'list_findings',
                'list_analyzed_resources'
            )
        ]
    )

    client = module.client('accessanalyzer')
    __default_return = []

    _it, paginate = _iam_access_analyzer(client, module)
    if _it is not None:
        if module.params['list_analyzers']:
            module.exit_json(analyzers=aws_response_list_parser(paginate, _it, 'analyzers'))
        elif module.params['list_archive_rules']:
            module.exit_json(archive_rules=aws_response_list_parser(paginate, _it, 'archiveRules'))
        elif module.params['list_findings']:
            module.exit_json(findings=aws_response_list_parser(paginate, _it, 'findings'))
        elif module.params['list_analyzed_resources']:
            module.exit_json(analyzed_resources=aws_response_list_parser(paginate, _it, 'analyzedResources'))


if __name__ == '__main__':
    main()
