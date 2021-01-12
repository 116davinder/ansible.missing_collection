#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_codeguru_reviewer_info
short_description: Get Information about AWS Codeguru Reviewer.
description:
  - Get Information about AWS Codeguru Reviewer.
  - U(https://docs.aws.amazon.com/codeguru/latest/reviewer-api/API_Operations.html)
version_added: 0.0.3
options:
  arn:
    description:
      - Arn of code review.
    required: false
    type: str
  type:
    description:
      - The type of code reviews.
    required: false
    type: str
    choices: ['PullRequest', 'RepositoryAnalysis']
  provider_types:
    description:
      - provider_types to filter resources.
      - can be combination of 'CodeCommit', 'GitHub', 'Bitbucket', 'GitHubEnterpriseServer' for I(list_code_reviews)?
      - can be combination of 'Associated', 'Associating', 'Failed', 'Disassociating', 'Disassociated' for I(list_repository_associations)?
    required: false
    type: list
  states:
    description:
      - state to filter resources.
      - can be combination of 'Completed', 'Pending', 'Failed', 'Deleting'?
    required: false
    type: list
  repository_names:
    description:
      - list of repository names?
    required: false
    type: list
  describe_code_review:
    description:
      - do you want to describe I(arn)?
    required: false
    type: bool
  list_code_reviews:
    description:
      - do you want to list code review for given I(type), I(provider_types), I(states), and I(repository_names)?
    required: false
    type: bool
  list_recommendation_feedback:
    description:
      - do you want to get list of recommendation feedback for given I(arn)?
    required: false
    type: bool
  list_recommendations:
    description:
      - do you want to get list of recommendation for given I(arn)?
    required: false
    type: bool
  list_repository_associations:
    description:
      - do you want to get list of repository associations feedback for given I(provider_types), I(states), and I(repository_names)?
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
- name: "get list of code reviews"
  aws_codeguru_reviewer_info:
    list_code_reviews: true
    provider_types: ['CodeCommit']
    type: 'PullRequest'
    states: ['Completed']
    repository_names: ['test']

- name: "get details about given code review arn"
  aws_codeguru_reviewer_info:
    describe_code_review: true
    arn: 'arn:aws:::codeguru-reviewer:test'

- name: "get list of recommendations about given code review arn"
  aws_codeguru_reviewer_info:
    list_recommendations: true
    arn: 'arn:aws:::codeguru-reviewer:test'

- name: "get list of recommendations feedback about given code review arn"
  aws_codeguru_reviewer_info:
    list_recommendation_feedback: true
    arn: 'arn:aws:::codeguru-reviewer:test'

- name: "get list repository associations"
  aws_codeguru_reviewer_info:
    list_repository_associations: true
    provider_types: ['CodeCommit']
    states: ['Associated']
    repository_names: ['test']
"""

RETURN = """
code_review:
  description: get details about code review.
  returned: when `arn` is defined and success
  type: dict
  sample: {
    'name': 'string',
    'code_review_arn': 'string',
    'repository_name': 'string',
    'owner': 'string',
    'provider_type': 'CodeCommit',
    'state': 'Completed',
    'state_reason': 'string',
    'created_time_stamp': datetime(2016, 6, 6),
    'last_updated_time_stamp': datetime(2015, 1, 1),
    'type': 'PullRequest',
    'pull_request_id': 'string',
    'sourceCode_type': {},
    'association_arn': 'string',
    'metrics': {}
  }
code_review_summaries:
  description: list of code review summaries.
  returned: when `list_code_reviews`, `type`, `provider_types`, `states`, and `repository_names` are defined and success
  type: list
  sample: [
    {
        'name': 'string',
        'code_review_arn': 'string',
        'repository_name': 'string',
        'owner': 'string',
        'provider_type': 'CodeCommit',
        'state': 'Completed',
        'created_time_stamp': datetime(2016, 6, 6),
        'last_updated_time_stamp': datetime(2015, 1, 1),
        'type': 'PullRequest',
        'pull_request_id': 'string',
        'metrics_summary': {}
    },
  ]
recommendation_feedback_summaries:
  description: list of code recommendation feedback summaries.
  returned: when `list_recommendation_feedback`, and `arn` are defined and success
  type: list
  sample: [
    {
        'recommendation_id': 'string',
        'reactions': [
            'ThumbsUp',
        ],
        'user_id': 'string'
    },
  ]
recommendation_summaries:
  description: list of code recommendation summaries.
  returned: when `list_recommendations`, and `arn` are defined and success
  type: list
  sample: [
    {
        'file_path': 'string',
        'recommendation_id': 'string',
        'start_line': 123,
        'end_line': 123,
        'description': 'string'
    },
  ]
repository_association_summaries:
  description: list of code repository association summaries.
  returned: when `list_repository_associations`, `provider_types`, `states`, and `repository_names` are defined and success
  type: list
  sample: [
    {
        'association_arn': 'string',
        'connection_arn': 'string',
        'last_updated_time_stamp': datetime(2015, 1, 1),
        'association_id': 'string',
        'name': 'string',
        'owner': 'string',
        'provider_type': 'CodeCommit',
        'state': 'Associated'
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


def _codeguru(client, module):
    try:
        if module.params['describe_code_review']:
            return client.describe_code_review(
                CodeReviewArn=module.params['arn']
            ), False
        elif module.params['list_code_reviews']:
            if client.can_paginate('list_code_reviews'):
                paginator = client.get_paginator('list_code_reviews')
                return paginator.paginate(
                    ProviderTypes=module.params['provider_types'],
                    States=module.params['states'],
                    RepositoryNames=module.params['repository_names'],
                    Type=module.params['type']
                ), True
            else:
                return client.list_code_reviews(
                    ProviderTypes=module.params['provider_types'],
                    States=module.params['states'],
                    RepositoryNames=module.params['repository_names'],
                    Type=module.params['type']
                ), False
        elif module.params['list_recommendation_feedback']:
            if client.can_paginate('list_recommendation_feedback'):
                paginator = client.get_paginator('list_recommendation_feedback')
                return paginator.paginate(
                    CodeReviewArn=module.params['arn']
                ), True
            else:
                return client.list_recommendation_feedback(
                    CodeReviewArn=module.params['arn']
                ), False
        elif module.params['list_recommendations']:
            if client.can_paginate('list_recommendations'):
                paginator = client.get_paginator('list_recommendations')
                return paginator.paginate(
                    CodeReviewArn=module.params['arn']
                ), True
            else:
                return client.list_recommendations(
                    CodeReviewArn=module.params['arn']
                ), False
        elif module.params['list_repository_associations']:
            if client.can_paginate('list_repository_associations'):
                paginator = client.get_paginator('list_repository_associations')
                return paginator.paginate(
                    ProviderTypes=module.params['provider_types'],
                    States=module.params['states'],
                    Names=module.params['repository_names'],
                ), True
            else:
                return client.list_repository_associations(
                    ProviderTypes=module.params['provider_types'],
                    States=module.params['states'],
                    Names=module.params['repository_names'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws codeguru reviewer details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        type=dict(required=False, choices=['PullRequest', 'RepositoryAnalysis']),
        provider_types=dict(required=False, type=list),
        states=dict(required=False, type=list),
        repository_names=dict(required=False, type=list),
        describe_code_review=dict(required=False, type=bool),
        list_code_reviews=dict(required=False, type=bool),
        list_recommendation_feedback=dict(required=False, type=bool),
        list_recommendations=dict(required=False, type=bool),
        list_repository_associations=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('describe_code_review', True, ['arn']),
            ('list_recommendation_feedback', True, ['arn']),
            ('list_recommendations', True, ['arn']),
            ('list_code_reviews', True, ['type', 'provider_types', 'states', 'repository_names']),
            ('list_repository_associations', True, ['provider_types', 'states', 'repository_names']),
        ),
        mutually_exclusive=[
            (
                'describe_code_review',
                'list_code_reviews',
                'list_recommendation_feedback',
                'list_recommendations',
                'list_repository_associations',
            )
        ],
    )

    client = module.client('codeguru-reviewer', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _codeguru(client, module)

    if module.params['describe_code_review']:
        module.exit_json(code_review=camel_dict_to_snake_dict(_it['CodeReview']))
    elif module.params['list_code_reviews']:
        module.exit_json(code_review_summaries=aws_response_list_parser(paginate, _it, 'CodeReviewSummaries'))
    elif module.params['list_recommendation_feedback']:
        module.exit_json(recommendation_feedback_summaries=aws_response_list_parser(paginate, _it, 'RecommendationFeedbackSummaries'))
    elif module.params['list_recommendations']:
        module.exit_json(recommendation_summaries=aws_response_list_parser(paginate, _it, 'RecommendationSummaries'))
    elif module.params['list_repository_associations']:
        module.exit_json(repository_association_summaries=aws_response_list_parser(paginate, _it, 'RepositoryAssociationSummaries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
