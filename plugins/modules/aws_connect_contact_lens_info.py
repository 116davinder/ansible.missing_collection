#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_connect_contact_lens_info
short_description: Get Information about Amazon Connect Contact Lens.
description:
  - Get Information about Amazon Connect Contact Lens.
  - U(https://docs.aws.amazon.com/contact-lens/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  instance_id:
    description:
      - The identifier of the Amazon Connect instance.
    required: false
    type: str
  contact_id:
    description:
      - The identifier of the contact.
    required: false
    type: str
  list_realtime_contact_analysis_segments:
    description:
      - do you want to get  list of analysis segments for a real-time analysis session?
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
- name: "get analysis segments of real time session"
  aws_connect_contact_lens_info:
    list_realtime_contact_analysis_segments: true
    instance_id: 'test-instance'
    contact_id: 'test-contact'
"""

RETURN = """
segments:
  description: list of analysis segments for real-time session.
  returned: when `list_realtime_contact_analysis_segments`, `instance_id`, and `contact_id` are defined and success
  type: list
  sample: [
    {
        'transcript': {
            'id': 'string',
            'participant_id': 'string',
            'participant_role': 'string',
            'content': 'string',
            'begin_offset_millis': 123,
            'end_offset_millis': 123,
            'sentiment': 'POSITIVE',
            'issues_detected': []
        },
        'categories': {
            'matched_categories': [],
            'matched_details': {}
        }
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


def _connect(client, module):
    try:
        if module.params['list_realtime_contact_analysis_segments']:
            if client.can_paginate('list_realtime_contact_analysis_segments'):
                paginator = client.get_paginator('list_realtime_contact_analysis_segments')
                return paginator.paginate(
                    InstanceId=module.params['instance_id'],
                    ContactId=module.params['contact_id'],
                ), True
            else:
                return client.list_realtime_contact_analysis_segments(
                    InstanceId=module.params['instance_id'],
                    ContactId=module.params['contact_id'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws connect contact lens details')


def main():
    argument_spec = dict(
        instance_id=dict(required=False),
        contact_id=dict(required=False),
        list_realtime_contact_analysis_segments=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_realtime_contact_analysis_segments', True, ['instance_id', 'contact_id']),
        ),
        mutually_exclusive=[],
    )

    client = module.client('connect-contact-lens', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _connect(client, module)

    if module.params['list_realtime_contact_analysis_segments']:
        module.exit_json(segments=aws_response_list_parser(paginate, _it, 'Segments'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
