#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_comprehendmedical_info
short_description: Get Information about Amazon Comprehend Medical.
description:
  - Get Information about Amazon Comprehend Medical.
  - U(https://docs.aws.amazon.com/comprehend/latest/dg/API_Operations_Amazon_Comprehend_Medical.html)
version_added: 0.0.4
options:
  job_status:
    description:
      - status of the job to filter results.
    required: false
    type: str
    choices: ["SUBMITTED", "IN_PROGRESS", "COMPLETED", "FAILED", "STOP_REQUESTED", "STOPPED", "PARTIAL_SUCCESS"]
    default: "IN_PROGRESS"
  list_entities_detection_v2_jobs:
    description:
      - do you want to get list of events detection v2 jobs for given I(job_status)?
    required: false
    type: bool
  list_icd10_cm_inference_jobs:
    description:
      - do you want to get list of icd10 cm inference jobs for given I(job_status)?
    required: false
    type: bool
  list_phi_detection_jobs:
    description:
      - do you want to get list of phi detection jobs for given I(job_status)?
    required: false
    type: bool
  list_rx_norm_inference_jobs:
    description:
      - do you want to get list of rx norm inference jobs for given I(job_status)?
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
- name: "get list of comprehendmedical entities detection v2 jobs"
  aws_comprehendmedical_info:
    list_entities_detection_v2_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehendmedical icd10 cm inference jobs"
  aws_comprehendmedical_info:
    list_icd10_cm_inference_jobs: true

- name: "get list of comprehendmedical phi detection jobs"
  aws_comprehendmedical_info:
    list_phi_detection_jobs: true
    job_status: "SUBMITTED"

- name: "get list of comprehendmedical rx norm inference jobs"
  aws_comprehendmedical_info:
    list_rx_norm_inference_jobs: true
    job_status: "SUBMITTED"
"""

RETURN = """
entities_detection_v2_jobs:
  description: get list of comprehendmedical entities detection v2 jobs.
  returned: when `list_entities_detection_v2_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2017, 7, 7),
        'expiration_time': datetime(2015, 1, 1),
        'input_data_config': {},
        'output_data_config': {},
        'language_code': 'en',
        'data_access_role_arn': 'string',
        'manifest_file_path': 'string',
        'kms_key': 'string',
        'model_version': 'string'
    },
  ]
icd10_cm_inference_jobs:
  description: get list of comprehendmedical icd10 cm inference jobs.
  returned: when `list_icd10_cm_inference_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2017, 7, 7),
        'expiration_time': datetime(2015, 1, 1),
        'input_data_config': {},
        'output_data_config': {},
        'language_code': 'en',
        'data_access_role_arn': 'string',
        'manifest_file_path': 'string',
        'kms_key': 'string',
        'model_version': 'string'
    },
  ]
phi_detection_jobs:
  description: get list of comprehendmedical phi detection jobs.
  returned: when `list_phi_detection_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2017, 7, 7),
        'expiration_time': datetime(2015, 1, 1),
        'input_data_config': {},
        'output_data_config': {},
        'language_code': 'en',
        'data_access_role_arn': 'string',
        'manifest_file_path': 'string',
        'kms_key': 'string',
        'model_version': 'string'
    },
  ]
rx_norm_inference_jobs:
  description: get list of comprehendmedical rx norm inference jobs.
  returned: when `list_rx_norm_inference_jobs` and `job_status` are defined and success
  type: list
  sample: [
    {
        'job_id': 'string',
        'job_name': 'string',
        'job_status': 'SUBMITTED',
        'message': 'string',
        'submit_time': datetime(2016, 6, 6),
        'end_time': datetime(2017, 7, 7),
        'expiration_time': datetime(2015, 1, 1),
        'input_data_config': {},
        'output_data_config': {},
        'language_code': 'en',
        'data_access_role_arn': 'string',
        'manifest_file_path': 'string',
        'kms_key': 'string',
        'model_version': 'string'
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


def _comprehendmedical(client, module):
    try:
        if module.params['list_entities_detection_v2_jobs']:
            if client.can_paginate('list_entities_detection_v2_jobs'):
                paginator = client.get_paginator('list_entities_detection_v2_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_entities_detection_v2_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_icd10_cm_inference_jobs']:
            if client.can_paginate('list_icd10_cm_inference_jobs'):
                paginator = client.get_paginator('list_icd10_cm_inference_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_entities_detection_v2_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_phi_detection_jobs']:
            if client.can_paginate('list_phi_detection_jobs'):
                paginator = client.get_paginator('list_phi_detection_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_phi_detection_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        elif module.params['list_rx_norm_inference_jobs']:
            if client.can_paginate('list_rx_norm_inference_jobs'):
                paginator = client.get_paginator('list_rx_norm_inference_jobs')
                return paginator.paginate(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), True
            else:
                return client.list_rx_norm_inference_jobs(
                    Filter={
                        'JobStatus': module.params['job_status']
                    }
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws comprehendmedical details')


def main():
    argument_spec = dict(
        job_status=dict(
            required=False,
            choices=["SUBMITTED", "IN_PROGRESS", "COMPLETED", "FAILED", "STOP_REQUESTED", "STOPPED", "PARTIAL_SUCCESS"],
            default="IN_PROGRESS"
        ),
        list_entities_detection_v2_jobs=dict(required=False, type=bool),
        list_icd10_cm_inference_jobs=dict(required=False, type=bool),
        list_phi_detection_jobs=dict(required=False, type=bool),
        list_rx_norm_inference_jobs=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(),
        mutually_exclusive=[
            (
                'list_entities_detection_v2_jobs',
                'list_icd10_cm_inference_jobs',
                'list_phi_detection_jobs',
                'list_rx_norm_inference_jobs',
            )
        ],
    )

    client = module.client('comprehendmedical', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _comprehendmedical(client, module)

    if module.params['list_entities_detection_v2_jobs']:
        module.exit_json(entities_detection_v2_jobs=aws_response_list_parser(paginate, _it, 'ComprehendMedicalAsyncJobPropertiesList'))
    elif module.params['list_icd10_cm_inference_jobs']:
        module.exit_json(icd10_cm_inference_jobs=aws_response_list_parser(paginate, _it, 'ComprehendMedicalAsyncJobPropertiesList'))
    elif module.params['list_phi_detection_jobs']:
        module.exit_json(phi_detection_jobs=aws_response_list_parser(paginate, _it, 'ComprehendMedicalAsyncJobPropertiesList'))
    elif module.params['list_rx_norm_inference_jobs']:
        module.exit_json(rx_norm_inference_jobs=aws_response_list_parser(paginate, _it, 'ComprehendMedicalAsyncJobPropertiesList'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
