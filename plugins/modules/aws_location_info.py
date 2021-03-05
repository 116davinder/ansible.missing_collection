#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_location_info
short_description: Get Information about Amazon Location Service.
description:
  - Get Information about Amazon Location Service.
  - U(https://docs.aws.amazon.com/location/index.html)
version_added: 0.0.7
options:
  name:
    description:
      - can be name of collection?
      - can be name of tracker?
    required: false
    type: str
    aliases: ['collection_name', 'tracker_name']
  list_geofence_collections:
    description:
      - do you want to get list of geofence_collections?
    required: false
    type: bool
  list_geofences:
    description:
      - do you want to get list of geofences for given collection I(name)?
    required: false
    type: bool
  list_maps:
    description:
      - do you want to get list of maps?
    required: false
    type: bool
  list_place_indexes:
    description:
      - do you want to get list of place_indexes?
    required: false
    type: bool
  list_tracker_consumers:
    description:
      - do you want to get list of tracker_consumers for given tracker I(name)?
    required: false
    type: bool
  list_trackers:
    description:
      - do you want to get list of trackers?
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
- name: "get list of geofence_collections"
  aws_location_info:
    list_geofence_collections: true

- name: "get list of geofences"
  aws_location_info:
    list_geofences: true
    name: 'test-collection-name'

- name: "get list of maps"
  aws_location_info:
    list_maps: true

- name: "get list of place_indexes"
  aws_location_info:
    list_place_indexes: true

- name: "get list of tracker_consumers"
  aws_location_info:
    list_tracker_consumers: true
    name: 'test-tracker-name'

- name: "get list of trackers"
  aws_location_info:
    list_trackers: true
"""

RETURN = """
geofence_collections:
  description: list of geofence_collections.
  returned: when `list_geofence_collections` is defined and success.
  type: list
geofences:
  description: list of geofences.
  returned: when `list_geofences` is defined and success.
  type: list
maps:
  description: list of maps.
  returned: when `list_maps` is defined and success.
  type: list
place_indexes:
  description: list of place_indexes.
  returned: when `list_place_indexes` is defined and success.
  type: list
tracker_consumers:
  description: list of tracker_consumers.
  returned: when `list_tracker_consumers` is defined and success.
  type: list
trackers:
  description: list of trackers.
  returned: when `list_trackers` is defined and success.
  type: list
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _location(client, module):
    try:
        if module.params['list_geofence_collections']:
            if client.can_paginate('list_geofence_collections'):
                paginator = client.get_paginator('list_geofence_collections')
                return paginator.paginate(), True
            else:
                return client.list_geofence_collections(), False
        elif module.params['list_geofences']:
            if client.can_paginate('list_geofences'):
                paginator = client.get_paginator('list_geofences')
                return paginator.paginate(
                    CollectionName=module.params['name']
                ), True
            else:
                return client.list_geofences(
                    CollectionName=module.params['name']
                ), False
        elif module.params['list_maps']:
            if client.can_paginate('list_maps'):
                paginator = client.get_paginator('list_maps')
                return paginator.paginate(), True
            else:
                return client.list_maps(), False
        elif module.params['list_place_indexes']:
            if client.can_paginate('list_place_indexes'):
                paginator = client.get_paginator('list_place_indexes')
                return paginator.paginate(), True
            else:
                return client.list_place_indexes(), False
        elif module.params['list_tracker_consumers']:
            if client.can_paginate('list_tracker_consumers'):
                paginator = client.get_paginator('list_tracker_consumers')
                return paginator.paginate(
                    TrackerName=module.params['name'],
                ), True
            else:
                return client.list_tracker_consumers(
                    TrackerName=module.params['name'],
                ), False
        elif module.params['list_trackers']:
            if client.can_paginate('list_trackers'):
                paginator = client.get_paginator('list_trackers')
                return paginator.paginate(), True
            else:
                return client.list_trackers(), False
        else:
            return None, False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch Amazon Location Service details')


def main():
    argument_spec = dict(
        name=dict(required=False, aliases=['collection_name', 'tracker_ame']),
        list_geofence_collections=dict(required=False, type=bool),
        list_geofences=dict(required=False, type=bool),
        list_maps=dict(required=False, type=bool),
        list_place_indexes=dict(required=False, type=bool),
        list_tracker_consumers=dict(required=False, type=bool),
        list_trackers=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=(
            ('list_geofences', True, ['name']),
            ('list_tracker_consumers', True, ['name']),
        ),
        mutually_exclusive=[
            (
                'list_geofence_collections',
                'list_geofences',
                'list_maps',
                'list_place_indexes',
                'list_tracker_consumers',
                'list_trackers',
            )
        ],
    )

    client = module.client('location', retry_decorator=AWSRetry.exponential_backoff())
    it, paginate = _location(client, module)

    if module.params['list_geofence_collections']:
        module.exit_json(geofence_collections=aws_response_list_parser(paginate, it, 'Entries'))
    elif module.params['list_geofences']:
        module.exit_json(geofences=aws_response_list_parser(paginate, it, 'Entries'))
    elif module.params['list_maps']:
        module.exit_json(maps=aws_response_list_parser(paginate, it, 'Entries'))
    elif module.params['list_place_indexes']:
        module.exit_json(place_indexes=aws_response_list_parser(paginate, it, 'Entries'))
    elif module.params['list_tracker_consumers']:
        module.exit_json(tracker_consumers=aws_response_list_parser(paginate, it, 'ConsumerArns'))
    elif module.params['list_trackers']:
        module.exit_json(trackers=aws_response_list_parser(paginate, it, 'Entries'))
    else:
        module.fail_json("unknown options are passed")


if __name__ == '__main__':
    main()
