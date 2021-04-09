#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_rekognition_info
short_description: Get Information about Amazon Rekognition.
description:
  - Get Information about Amazon Rekognition.
  - U(https://docs.aws.amazon.com/rekognition/latest/dg/API_Operations.html)
version_added: 0.0.8
options:
  id:
    description:
      - collection id.
    required: false
    type: str
    aliases: ['collection_id']
  list_collections:
    description:
      - do you want to get list of collections?
    required: false
    type: bool
  list_faces:
    description:
      - do you want to get faces for given I(id)?
    required: false
    type: bool
  list_stream_processors:
    description:
      - do you want to get list of stream_processors?
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
- name: "get list of collections"
  aws_rekognition_info:
    list_collections: true

- name: "get list of faces"
  aws_rekognition_info:
    list_faces: true
    id: 'collection_id'

- name: "get list of stream_processors"
  aws_rekognition_info:
    list_stream_processors: true
"""

RETURN = """
collections:
  description: list of collections.
  returned: when `list_collections` is defined and success.
  type: list
faces:
  description: get of faces.
  returned: when `list_faces` is defined and success.
  type: list
stream_processors:
  description: list of stream_processors.
  returned: when `list_stream_processors` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _rekognition(client, module):
    try:
        if module.params['list_collections']:
            if client.can_paginate('list_collections'):
                paginator = client.get_paginator('list_collections')
                return paginator.paginate(), True
            else:
                return client.list_collections(), False
        elif module.params['list_faces']:
            if client.can_paginate('list_faces'):
                paginator = client.get_paginator('list_faces')
                return paginator.paginate(
                    CollectionId=module.params['id'],
                ), True
            else:
                return client.list_faces(
                    CollectionId=module.params['id'],
                ), False
        elif module.params['list_stream_processors']:
            if client.can_paginate('list_stream_processors'):
                paginator = client.get_paginator('list_stream_processors')
                return paginator.paginate(
                    Status=module.params['status']
                ), True
            else:
                return client.list_stream_processors(
                    Status=module.params['status']
                ), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Rekognition details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['collection_id']),
        list_collections=dict(required=False, type=bool),
        list_faces=dict(required=False, type=bool),
        list_stream_processors=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_faces', True, ['id']),
        ),
        mutually_exclusive=[
            (
                'list_collections',
                'list_faces',
                'list_stream_processors',
            )
        ],
    )

    client = module.client('rekognition', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _rekognition(client, module)

    if module.params['list_collections']:
        module.exit_json(collections=aws_response_list_parser(paginate, it, 'CollectionIds'))
    elif module.params['list_faces']:
        module.exit_json(faces=aws_response_list_parser(paginate, it, 'Faces'))
    elif module.params['list_stream_processors']:
        module.exit_json(stream_processors=aws_response_list_parser(paginate, it, 'StreamProcessors'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
