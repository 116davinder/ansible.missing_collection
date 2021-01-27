#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_comprehend_info
short_description: Get Information about Amazon Comprehend.
description:
  - Get Information about Amazon Comprehend.
  - U(https://docs.aws.amazon.com/comprehend/latest/dg/API_Operations_Amazon_Comprehend.html)
version_added: 0.0.4
options:
  job_status:
    description:
      - status of the job to filter results.
    required: false
    type: str
    choices: ["SUBMITTED", "IN_PROGRESS", "COMPLETED", "FAILED", "STOP_REQUESTED", "STOPPED"]
    default: "IN_PROGRESS"
  list_document_classification_jobs:
    description:
      - do you want to get list of document classification jobs for given I(job_status)?
    required: false
    type: bool
  list_document_classifiers:
    description:
      - do you want to get list of document classifiers?
    required: false
    type: bool
  list_dominant_language_detection_jobs:
    description:
      - do you want to get list of dominant language detection jobs for given I(job_status)?
    required: false
    type: bool
  list_entities_detection_jobs:
    description:
      - do you want to get list of entities detection jobs for given I(job_status)?
    required: false
    type: bool
  list_entity_recognizers:
    description:
      - do you want to get list of entity recognizers?
    required: false
    type: bool
  list_events_detection_jobs:
    description:
      - do you want to get list of events detection jobs for given I(job_status)?
    required: false
    type: bool
  list_key_phrases_detection_jobs:
    description:
      - do you want to get list of key phrases detection jobs for given I(job_status)?
    required: false
    type: bool
  list_pii_entities_detection_jobs:
    description:
      - do you want to get list of pii entities detection jobs for given I(job_status)?
    required: false
    type: bool
  list_sentiment_detection_jobs:
    description:
      - do you want to get list of sentiment detection jobs for given I(job_status)?
    required: false
    type: bool
  list_topics_detection_jobs:
    description:
      - do you want to get list of topics detection jobs for given I(job_status)?
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
- name: "get list of comprehend endpoints"
  aws_comprehend_info:

- name: "get list of comprehend document classification jobs"
  aws_comprehend_info:
    list_document_classification_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend document classifiers"
  aws_comprehend_info:
    list_document_classifiers: true

- name: "get list of comprehend dominant language detection jobs"
  aws_comprehend_info:
    list_dominant_language_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend entities detection jobs"
  aws_comprehend_info:
    list_entities_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend entity recognizers"
  aws_comprehend_info:
    list_entity_recognizers: true

- name: "get list of comprehend events detection jobs"
  aws_comprehend_info:
    list_events_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend key phrases detection jobs"
  aws_comprehend_info:
    list_key_phrases_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend pii entities detection jobs"
  aws_comprehend_info:
    list_pii_entities_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend sentiment detection jobs"
  aws_comprehend_info:
    list_sentiment_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehend topic detection jobs"
  aws_comprehend_info:
    list_topics_detection_jobs: true
    job_status: "SUBMITTED"
"""

RETURN = """
endpoints:
  description: lit of endpoints.
  returned: when no argument are defined and success
  type: list
  sample: [
    {
        'endpoint_arn': 'string',
        'status': 'CREATING',
        'message': 'string',
        'model_arn': 'string',
        'desired_inference_units': 1234,
        'current_inference_units': 123,
        'creation_time': datetime(2016, 6, 6),
        'last_modified_Time': datetime(2015, 1, 1)
    },
  ]
document_classification_jobs:
  description: get list of document classification jobs.
  returned: when `list_document_classification_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
document_classifiers:
  description: get list of document classifiers.
  returned: when `list_document_classifiers` is defined and success
  type: list
  sample: [
    {
        'document_classifier_arn': 'string',
        'language_code': 'en',
        'status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'training_start_time': datetime(2017, 7, 7),
        'training_end_time': datetime(2018, 8, 8),
        'input_data_config': {},
        'output_data_config': {},
        'classifierMetadata': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {},
        'mode': 'MULTI_CLASS'
    },
  ]
language_detection_jobs:
  description: get list of language detection jobs.
  returned: when `list_language_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
entities_detection_jobs:
  description: get list of entities detection jobs.
  returned: when `list_entities_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
entity_recognizers:
  description: get list of entity recognizers.
  returned: when `list_entity_recognizers` is defined and success
  type: list
  sample: [
    {
        'entity_recognizer_arn': 'string',
        'language_code': 'en',
        'status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'training_Start_time': datetime(2017, 7, 7),
        'training_end_time': datetime(2018, 8, 8),
        'input_data_config': {},
        'RecognizerMetadata': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
events_detection_jobs:
  description: get list of event detection jobs.
  returned: when `list_events_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
key_phrases_detection_jobs:
  description: get list of key phrases detection jobs.
  returned: when `list_key_phrases_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
pii_entities_detection_jobs:
  description: get list of pii entities detection jobs.
  returned: when `list_pii_entities_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
sentiment_detection_jobs:
  description: get list of sentiment detection jobs.
  returned: when `list_sentiment_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
topics_detection_jobs:
  description: get list of topics detection jobs.
  returned: when `list_topics_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2015, 1, 1),
        'document_classifier_arn': 'string',
        'input_data_config': {},
        'output_data_config': {},
        'data_access_role_arn': 'string',
        'volume_kms_key_id': 'string',
        'vpc_config': {}
    },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _comprehend(client, module):
    try:
        if module.params['list_document_classification_jobs']:
            if client.can_paginate('list_document_classification_jobs'):
                paginator = client.get_paginator('list_document_classification_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_document_classification_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_document_classifiers']:
            if client.can_paginate('list_document_classifiers'):
                paginator = client.get_paginator('list_document_classifiers')
                return paginator.paginate(), True
            else:
                return client.list_document_classifiers(), False
        elif module.params['list_dominant_language_detection_jobs']:
            if client.can_paginate('list_dominant_language_detection_jobs'):
                paginator = client.get_paginator('list_dominant_language_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_document_classifiers(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_entities_detection_jobs']:
            if client.can_paginate('list_entities_detection_jobs'):
                paginator = client.get_paginator('list_entities_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_entities_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_entity_recognizers']:
            if client.can_paginate('list_entity_recognizers'):
                paginator = client.get_paginator('list_entity_recognizers')
                return paginator.paginate(), True
            else:
                return client.list_entity_recognizers(), False
        elif module.params['list_events_detection_jobs']:
            if client.can_paginate('list_events_detection_jobs'):
                paginator = client.get_paginator('list_events_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_events_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_key_phrases_detection_jobs']:
            if client.can_paginate('list_key_phrases_detection_jobs'):
                paginator = client.get_paginator('list_key_phrases_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_key_phrases_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_pii_entities_detection_jobs']:
            if client.can_paginate('list_pii_entities_detection_jobs'):
                paginator = client.get_paginator('list_pii_entities_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_pii_entities_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_sentiment_detection_jobs']:
            if client.can_paginate('list_sentiment_detection_jobs'):
                paginator = client.get_paginator('list_sentiment_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_sentiment_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_topics_detection_jobs']:
            if client.can_paginate('list_topics_detection_jobs'):
                paginator = client.get_paginator('list_topics_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_topics_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        else:
            if client.can_paginate('list_endpoints'):
                paginator = client.get_paginator('list_endpoints')
                return paginator.paginate(), True
            else:
                return client.list_endpoints(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws comprehend details')


def main():
    argument_spec = dict(
        job_status=dict(
            required=False,
            choices=["SUBMITTED", "IN_PROGRESS", "COMPLETED", "FAILED", "STOP_REQUESTED", "STOPPED"],
            default="IN_PROGRESS"
        ),
        list_document_classification_jobs=dict(required=False, type=bool),
        list_document_classifiers=dict(required=False, type=bool),
        list_dominant_language_detection_jobs=dict(required=False, type=bool),
        list_entities_detection_jobs=dict(required=False, type=bool),
        list_entity_recognizers=dict(required=False, type=bool),
        list_events_detection_jobs=dict(required=False, type=bool),
        list_key_phrases_detection_jobs=dict(required=False, type=bool),
        list_pii_entities_detection_jobs=dict(required=False, type=bool),
        list_sentiment_detection_jobs=dict(required=False, type=bool),
        list_topics_detection_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(),
        mutually_exclusive=[
            (
                'list_document_classification_jobs',
                'list_document_classifiers',
                'list_dominant_language_detection_jobs',
                'list_entities_detection_jobs',
                'list_entity_recognizers',
                'list_events_detection_jobs',
                'list_key_phrases_detection_jobs',
                'list_pii_entities_detection_jobs',
                'list_sentiment_detection_jobs',
                'list_topics_detection_jobs',
            )
        ],
    )

    client = module.client('comprehend', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _comprehend(client, module)

    if module.params['list_document_classification_jobs']:
        module.exit_json(document_classification_jobs=aws_response_list_parser(paginate, _it, 'DocumentClassificationJobPropertiesList'))
    elif module.params['list_document_classifiers']:
        module.exit_json(document_classifiers=aws_response_list_parser(paginate, _it, 'DocumentClassifierPropertiesList'))
    elif module.params['list_dominant_language_detection_jobs']:
        module.exit_json(language_detection_jobs=aws_response_list_parser(paginate, _it, 'DominantLanguageDetectionJobPropertiesList'))
    elif module.params['list_entities_detection_jobs']:
        module.exit_json(entities_detection_jobs=aws_response_list_parser(paginate, _it, 'EntitiesDetectionJobPropertiesList'))
    elif module.params['list_entity_recognizers']:
        module.exit_json(entity_recognizers=aws_response_list_parser(paginate, _it, 'EntityRecognizerPropertiesList'))
    elif module.params['list_events_detection_jobs']:
        module.exit_json(events_detection_jobs=aws_response_list_parser(paginate, _it, 'EventsDetectionJobPropertiesList'))
    elif module.params['list_key_phrases_detection_jobs']:
        module.exit_json(key_phrases_detection_jobs=aws_response_list_parser(paginate, _it, 'KeyPhrasesDetectionJobPropertiesList'))
    elif module.params['list_pii_entities_detection_jobs']:
        module.exit_json(pii_entities_detection_jobs=aws_response_list_parser(paginate, _it, 'PiiEntitiesDetectionJobPropertiesList'))
    elif module.params['list_sentiment_detection_jobs']:
        module.exit_json(sentiment_detection_jobs=aws_response_list_parser(paginate, _it, 'SentimentDetectionJobPropertiesList'))
    elif module.params['list_topics_detection_jobs']:
        module.exit_json(topics_detection_jobs=aws_response_list_parser(paginate, _it, 'TopicsDetectionJobPropertiesList'))
    else:
        module.exit_json(endpoints=aws_response_list_parser(paginate, _it, 'EndpointPropertiesList'))


if __name__ == '__main__':
    main()
