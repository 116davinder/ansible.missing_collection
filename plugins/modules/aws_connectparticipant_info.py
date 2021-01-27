#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_connectparticipant_info
short_description: Get Information about Amazon Connect Participant Service.
description:
  - Get Information about Amazon Connect Participant Service.
  - U(https://docs.aws.amazon.com/connect-participant/latest/APIReference/API_Operations.html)
version_added: 0.0.5
options:
  connection_token:
    description:
      - The authentication token associated with the participant's connection.
    required: false
    type: str
  attachment_id:
    description:
      - A unique identifier for the attachment.
    required: false
    type: str
  contact_id:
    description:
      - The contactId from the current contact chain for which transcript is needed.
    required: false
    type: str
  get_attachment:
    description:
      - do you want to get attachment url for given I(connection_token) and I(attachment_id)?
    required: false
    type: bool
  get_transcript:
    description:
      - do you want to get list of transcripts for given I(connection_token) and I(contact_id)?
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
- name: "get pre-signed URL for download of a completed attachment"
  aws_connectparticipant_info:
    get_attachment: true
    connection_token: 'test-token'
    attachment_id: 'test-attachment'

- name: "get list of transcript of the session"
  aws_connectparticipant_info:
    get_transcript: true
    connection_token: 'test-token'
    contact_id: 'test-contact'
"""

RETURN = """
attachment:
  description: Provides a pre-signed URL for download of a completed attachment.
  returned: when `get_attachment`, `connection_token`, and `attachment_id` are defined and success
  type: dict
  sample: {
    'url': 'string',
    'url_expiry': 'string'
  }
transcript:
  description: Retrieves a transcript of the session.
  returned: when `get_transcript`, `connection_token`, and `contact_id` are defined and success
  type: list
  sample: [
    {
        'absolute_time': 'string',
        'content': 'string',
        'content_type': 'string',
        'id': 'string',
        'type': 'TYPING',
        'participant_id': 'string',
        'display_name': 'string',
        'participant_role': 'AGENT',
        'attachments': []
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
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _connect(client, module):
    try:
        if module.params['get_attachment']:
            return client.get_attachment(
                AttachmentId=module.params['attachment_id'],
                ConnectionToken=module.params['connection_token'],
            ), False
        elif module.params['get_transcript']:
            if client.can_paginate('get_transcript'):
                paginator = client.get_paginator('get_transcript')
                return paginator.paginate(
                    ContactId=module.params['contact_id'],
                    ConnectionToken=module.params['connection_token'],
                ), True
            else:
                return client.get_transcript(
                    ContactId=module.params['contact_id'],
                    ConnectionToken=module.params['connection_token'],
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws connect participant details')


def main():
    argument_spec = dict(
        connection_token=dict(required=False),
        attachment_id=dict(required=False),
        contact_id=dict(required=False),
        get_attachment=dict(required=False, type=bool),
        get_transcript=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('get_attachment', True, ['connection_token', 'attachment_id']),
            ('get_transcript', True, ['connection_token', 'contact_id']),
        ),
        mutually_exclusive=[
            (
                'get_attachment',
                'get_transcript',
            )
        ],
    )

    client = module.client('connectparticipant', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _connect(client, module)

    if module.params['get_attachment']:
        module.exit_json(attachment=camel_dict_to_snake_dict(_it))
    elif module.params['get_transcript']:
        module.exit_json(transcript=aws_response_list_parser(paginate, _it, 'Transcript'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
