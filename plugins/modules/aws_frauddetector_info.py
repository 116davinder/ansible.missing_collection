#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_frauddetector_info
short_description: Get Information about Amazon Fraud Detector.
description:
  - Get Information about Amazon Fraud Detector.
  - U(https://docs.aws.amazon.com/frauddetector/latest/api/API_Operations.html)
version_added: 0.0.6
options:
  detector_id:
    description:
      - id of detector.
    required: false
    type: bool
  get_detectors:
    description:
      - do you want to get list of detectors?
    required: false
    type: bool
  get_entity_types:
    description:
      - do you want to get list of entity types?
    required: false
    type: bool
  get_event_types:
    description:
      - do you want to get list of event types?
    required: false
    type: bool
  get_external_models:
    description:
      - do you want to get list of external models?
    required: false
    type: bool
  get_labels:
    description:
      - do you want to get list of labels?
    required: false
    type: bool
  get_models:
    description:
      - do you want to get list of models?
    required: false
    type: bool
  get_outcomes:
    description:
      - do you want to get list of outcomes?
    required: false
    type: bool
  get_rules:
    description:
      - do you want to get list of rules?
    required: false
    type: bool
  get_variables:
    description:
      - do you want to get list of variables?
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
- name: "get list of detectors"
  aws_frauddetector_info:
    get_detectors: true

- name: "get list of get entity types"
  aws_frauddetector_info:
    get_entity_types: true

- name: "get list of event types"
  aws_frauddetector_info:
    get_event_types: true

- name: "get list of external models"
  aws_frauddetector_info:
    get_external_models: true

- name: "get list of labels"
  aws_frauddetector_info:
    get_labels: true

- name: "get list of models"
  aws_frauddetector_info:
    get_models: true

- name: "get list of outcomes"
  aws_frauddetector_info:
    get_outcomes: true

- name: "get list of rules"
  aws_frauddetector_info:
    get_rules: true
    detector_id: 'test'

- name: "get list of variables"
  aws_frauddetector_info:
    get_variables: true
"""

RETURN = """
detectors:
  description: list of detectors.
  returned: when `get_detectors` is defined and success
  type: list
entity_types:
  description: list of get entity types
  returned: when `get_entity_types` is defined and success
  type: list
event_types:
  description: list of event types
  returned: when `get_event_types` is defined and success
  type: list
external_models:
  description: list of external models
  returned: when `get_external_models` is defined and success
  type: list
labels:
  description: list of labels.
  returned: when `get_labels` is defined and success
  type: list
models:
  description: list of models.
  returned: when `get_models` is defined and success
  type: list
outcomes:
  description: list of outcomes.
  returned: when `get_outcomes` is defined and success
  type: list
rules:
  description: list of rules.
  returned: when `get_rules` is defined and success
  type: list
variables:
  description: list of variables.
  returned: when `get_variables` is defined and success
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _frauddetector(client, module):
    try:
        if module.params['get_detectors']:
            if client.can_paginate('get_detectors'):
                paginator = client.get_paginator('get_detectors')
                return paginator.paginate(), True
            else:
                return client.get_detectors(), False
        elif module.params['get_entity_types']:
            if client.can_paginate('get_entity_types'):
                paginator = client.get_paginator('get_entity_types')
                return paginator.paginate(), True
            else:
                return client.get_entity_types(), False
        elif module.params['get_event_types']:
            if client.can_paginate('get_event_types'):
                paginator = client.get_paginator('get_event_types')
                return paginator.paginate(), True
            else:
                return client.get_event_types(), False
        elif module.params['get_external_models']:
            if client.can_paginate('get_external_models'):
                paginator = client.get_paginator('get_external_models')
                return paginator.paginate(), True
            else:
                return client.get_external_models(), False
        elif module.params['get_labels']:
            if client.can_paginate('get_labels'):
                paginator = client.get_paginator('get_labels')
                return paginator.paginate(), True
            else:
                return client.get_labels(), False
        elif module.params['get_models']:
            if client.can_paginate('get_models'):
                paginator = client.get_paginator('get_models')
                return paginator.paginate(), True
            else:
                return client.get_models(), False
        elif module.params['get_outcomes']:
            if client.can_paginate('get_outcomes'):
                paginator = client.get_paginator('get_outcomes')
                return paginator.paginate(), True
            else:
                return client.get_outcomes(), False
        elif module.params['get_rules']:
            if client.can_paginate('get_rules'):
                paginator = client.get_paginator('get_rules')
                return paginator.paginate(
                    detectorId=module.params['detector_id'],
                ), True
            else:
                return client.get_rules(
                    detectorId=module.params['detector_id'],
                ), False
        elif module.params['get_variables']:
            if client.can_paginate('get_variables'):
                paginator = client.get_paginator('get_variables')
                return paginator.paginate(), True
            else:
                return client.get_variables(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon frauddetector details')


def main():
    argument_spec = dict(
        detector_id=dict(required=False),
        get_detectors=dict(required=False, type=bool),
        get_entity_types=dict(required=False, type=bool),
        get_event_types=dict(required=False, type=bool),
        get_external_models=dict(required=False, type=bool),
        get_labels=dict(required=False, type=bool),
        get_models=dict(required=False, type=bool),
        get_outcomes=dict(required=False, type=bool),
        get_rules=dict(required=False, type=bool),
        get_variables=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('get_rules', True, ['detector_id']),
        ),
        mutually_exclusive=[
            (
                'get_detectors',
                'get_entity_types',
                'get_event_types',
                'get_external_models',
                'get_labels',
                'get_models',
                'get_outcomes',
                'get_rules',
                'get_variables',
            )
        ],
    )

    client = module.client('frauddetector', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _frauddetector(client, module)

    if module.params['get_detectors']:
        module.exit_json(detectors=aws_response_list_parser(paginate, it, 'detectors'))
    elif module.params['get_entity_types']:
        module.exit_json(entity_types=aws_response_list_parser(paginate, it, 'entityTypes'))
    elif module.params['get_event_types']:
        module.exit_json(event_types=aws_response_list_parser(paginate, it, 'eventTypes'))
    elif module.params['get_external_models']:
        module.exit_json(external_models=aws_response_list_parser(paginate, it, 'externalModels'))
    elif module.params['get_labels']:
        module.exit_json(labels=aws_response_list_parser(paginate, it, 'labels'))
    elif module.params['get_models']:
        module.exit_json(models=aws_response_list_parser(paginate, it, 'models'))
    elif module.params['get_outcomes']:
        module.exit_json(outcomes=aws_response_list_parser(paginate, it, 'outcomes'))
    elif module.params['get_rules']:
        module.exit_json(rules=aws_response_list_parser(paginate, it, 'ruleDetails'))
    elif module.params['get_variables']:
        module.exit_json(variables=aws_response_list_parser(paginate, it, 'variables'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
