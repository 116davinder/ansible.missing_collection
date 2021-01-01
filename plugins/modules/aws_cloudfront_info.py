#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudfront_info
short_description: Get details about Amazon CloudFront.
description:
  - Get Information about Amazon CloudFront.
  - U(https://docs.aws.amazon.com/cloudfront/latest/APIReference/API_Operations.html)
version_added: 0.0.2
options:
  id:
    description:
      - cloudfront distribution id.
    required: false
    type: str
    aliases: ['distribution_id']
  type:
    description:
      - type of cache/origin_request policy.
    required: false
    type: str
    choices: ['managed', 'custom']
  list_cache_policies:
    description:
      - do you want to list cache policies for given I(type)?
    required: false
    type: bool
  list_cloud_front_origin_access_identities:
    description:
      - do you want to get list of origin access identities?
    required: false
    type: bool
  list_field_level_encryption_configs:
    description:
      - do you want to get list of field level encryption configs?
    required: false
    type: bool
  list_field_level_encryption_profiles:
    description:
      - do you want to get list of field level encryption profiles?
    required: false
    type: bool
  list_invalidations:
    description:
      - do you want to get list of invalidation for given I(id)?
    required: false
    type: bool
  list_key_groups:
    description:
      - do you want to get list of key groups?
    required: false
    type: bool
  list_origin_request_policies:
    description:
      - do you want to get list of origin request policies for given I(type)?
    required: false
    type: bool
  list_public_keys:
    description:
      - do you want to get list of public keys?
    required: false
    type: bool
  list_streaming_distributions:
    description:
      - do you want to get list of streaming distributions?
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
- name: "list of all cloudfront distributions ids"
  aws_cloudfront_info:
  register: _dl

- name: "list of cache policies"
  aws_cloudfront_info:
    type: 'managed'
    list_cache_policies: true

- name: "list of all orgins identities"
  aws_cloudfront_info:
    list_cloud_front_origin_access_identities: true

- name: "list of all field level encryption configs"
  aws_cloudfront_info:
    list_field_level_encryption_configs: true

- name: "list of all field level encryption profiles"
  aws_cloudfront_info:
    list_field_level_encryption_profiles: true

- name: "list of all field level encryption profiles"
  aws_cloudfront_info:
    id: "{{ _dl.distribution_list[0].id }}"
    list_invalidations: true

- name: "list of all key groups"
  aws_cloudfront_info:
    list_key_groups: true

- name: "list of all origin request policies"
  aws_cloudfront_info:
    type: 'managed'
    list_origin_request_policies: true

- name: "list of all public keys"
  aws_cloudfront_info:
    list_public_keys: true

- name: "list of all streaming distribution"
  aws_cloudfront_info:
    list_streaming_distributions: true
"""

RETURN = """
distribution_list:
  description: List CloudFront distributions.
  returned: when no argument and success
  type: list
  sample: [
      {
          'id': 'string',
          'arn': 'string',
          'status': 'string',
          'last_modified_time': datetime(2015, 1, 1),
          'domain_name': 'string',
          'aliases': {},
          'origins': {},
          'origin_groups': {},
          'default_cache_behavior': {},
          'cache_behaviors': {},
          'custom_error_responses': {},
          'comment': 'string',
          'price_class': 'PriceClass_100',
          'enabled': True,
          'viewer_certificate': {},
          'restrictions': {},
          'web_acl_id': 'string',
          'http_version': 'http2',
          'is_ipv6_enabled': True,
          'alias_icp_recordals': []
      },
  ]
cache_policy_list:
  description: Gets a list of cache policies.
  returned: when `list_cache_policies` and `type` are defined and success
  type: list
  sample: [
      {
          'type': 'managed',
          'cache_policy': {
              'id': 'string',
              'last_modified_time': datetime(2015, 1, 1),
              'cache_policy_config': {}
          }
      },
  ]
cloud_front_origin_access_identity_list:
  description: Lists origin access identities.
  returned: when `list_cloud_front_origin_access_identities` is defined and success
  type: list
  sample: [
      {
          '_d': 'string',
          's3_canonical_user_id': 'string',
          'comment': 'string'
      },
  ]
field_level_encryption_list:
  description: List all field-level encryption configurations that have been created in CloudFront for this account.
  returned: when `list_field_level_encryption_configs` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'last_modified_time': datetime(2015, 1, 1),
          'comment': 'string',
          'query_arg_profile_config': {},
          'content_type_profile_config': {}
      },
  ]
field_level_encryption_profile_list:
  description: Request a list of field-level encryption profiles that have been created in CloudFront for this account.
  returned: when `list_field_level_encryption_profiles` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'last_modified_time': datetime(2015, 1, 1),
          'name': 'string',
          'encryption_entities': {
              'quantity': 123,
              'items': []
          },
          'comment': 'string'
      },
  ]
invalidation_list:
  description: Lists invalidation batches.
  returned: when `list_invalidations` and `id` are defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'create_time': datetime(2015, 1, 1),
          'status': 'string'
      },
  ]
key_group_list:
  description: Gets a list of key groups.
  returned: when `list_key_groups` is defined and success
  type: list
  sample: [
      {
          'key_group': {
              'id': 'string',
              'last_modified_time': datetime(2015, 1, 1),
              'key_group_config': {
                  'name': 'string',
                  'items': [
                      'string',
                  ],
                  'comment': 'string'
              }
          }
      },
  ]
origin_request_policy_list:
  description: Gets a list of origin request policies.
  returned: when `list_origin_request_policies` is defined and success
  type: list
  sample: [
      {
          'type': 'managed',
          'origin_request_policy': {
              'id': 'string',
              'last_modified_time': datetime(2015, 1, 1),
              'origin_request_policy_config': {
                  'comment': 'string',
                  'name': 'string',
                  'headers_config': {},
                  'cookies_config': {},
                  'query_strings_config': {}
              }
          }
      },
  ]
public_key_list:
  description: List all public keys that have been added to CloudFront for this account.
  returned: when `list_public_keys` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'name': 'string',
          'created_time': datetime(2015, 1, 1),
          'encoded_key': 'string',
          'comment': 'string'
      },
  ]
streaming_distribution_list:
  description: List streaming distributions.
  returned: when `list_streaming_distributions` is defined and success
  type: list
  sample: [
      {
          'id': 'string',
          'arn': 'string',
          'status': 'string',
          'last_modified_time': datetime(2015, 1, 1),
          'domain_name': 'string',
          's3_origin': {},
          'aliases': {},
          'trusted_signers': {},
          'comment': 'string',
          'price_class': 'PriceClass_100',
          'enabled': True
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


def aws_cloudfornt_parser(paginate: bool, iterator, resource_field: str, nested_resource_field: str) -> list:
    _return = []
    __l_list = []

    try:
        if paginate:
            for app in iterator:
                __l_list += app[resource_field][nested_resource_field]

            iterator = {
                resource_field: __l_list
            }

            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
        else:
            for item in iterator[resource_field][nested_resource_field]:
                _return.append(camel_dict_to_snake_dict(item))
    except KeyError:
        # no need to handle empty response from aws
        # or
        # nested_resource_field is missing
        pass
    return _return


def _cloudfront(client, module) -> tuple:
    try:
        if module.params['list_cache_policies']:
            if client.can_paginate('list_cache_policies'):
                paginator = client.get_paginator('list_cache_policies')
                return paginator.paginate(
                    Type=module.params['type']
                ), True
            else:
                return client.list_cache_policies(
                    Type=module.params['type']
                ), False
        elif module.params['list_cloud_front_origin_access_identities']:
            if client.can_paginate('list_cloud_front_origin_access_identities'):
                paginator = client.get_paginator('list_cloud_front_origin_access_identities')
                return paginator.paginate(), True
            else:
                return client.list_cloud_front_origin_access_identities(), False
        elif module.params['list_field_level_encryption_configs']:
            if client.can_paginate('list_field_level_encryption_configs'):
                paginator = client.get_paginator('list_field_level_encryption_configs')
                return paginator.paginate(), True
            else:
                return client.list_field_level_encryption_configs(), False
        elif module.params['list_field_level_encryption_profiles']:
            if client.can_paginate('list_field_level_encryption_profiles'):
                paginator = client.get_paginator('list_field_level_encryption_profiles')
                return paginator.paginate(), True
            else:
                return client.list_field_level_encryption_profiles(), False
        elif module.params['list_invalidations']:
            if client.can_paginate('list_invalidations'):
                paginator = client.get_paginator('list_invalidations')
                return paginator.paginate(
                    DistributionId=module.params['id']
                ), True
            else:
                return client.list_invalidations(
                    DistributionId=module.params['id']
                ), False
        elif module.params['list_key_groups']:
            if client.can_paginate('list_key_groups'):
                paginator = client.get_paginator('list_key_groups')
                return paginator.paginate(), True
            else:
                return client.list_key_groups(), False
        elif module.params['list_origin_request_policies']:
            if client.can_paginate('list_origin_request_policies'):
                paginator = client.get_paginator('list_origin_request_policies')
                return paginator.paginate(
                    Type=module.params['type']
                ), True
            else:
                return client.list_origin_request_policies(
                    Type=module.params['type']
                ), False
        elif module.params['list_public_keys']:
            if client.can_paginate('list_public_keys'):
                paginator = client.get_paginator('list_public_keys')
                return paginator.paginate(), True
            else:
                return client.list_public_keys(), False
        elif module.params['list_streaming_distributions']:
            if client.can_paginate('list_streaming_distributions'):
                paginator = client.get_paginator('list_streaming_distributions')
                return paginator.paginate(), True
            else:
                return client.list_streaming_distributions(), False
        else:
            if client.can_paginate('list_distributions'):
                paginator = client.get_paginator('list_distributions')
                return paginator.paginate(), True
            else:
                return client.list_distributions(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudfront details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['distribution_id']),
        type=dict(required=False, choices=['managed', 'custom']),
        list_cache_policies=dict(required=False, type=bool),
        list_cloud_front_origin_access_identities=dict(required=False, type=bool),
        list_field_level_encryption_configs=dict(required=False, type=bool),
        list_field_level_encryption_profiles=dict(required=False, type=bool),
        list_invalidations=dict(required=False, type=bool),
        list_key_groups=dict(required=False, type=bool),
        list_origin_request_policies=dict(required=False, type=bool),
        list_public_keys=dict(required=False, type=bool),
        list_streaming_distributions=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('list_cache_policies', True, ['type']),
            ('list_invalidations', True, ['id']),
            ('list_origin_request_policies', True, ['type']),
        ],
        mutually_exclusive=[
            (
                'list_cache_policies',
                'list_cloud_front_origin_access_identities',
                'list_field_level_encryption_configs',
                'list_field_level_encryption_profiles',
                'list_invalidations',
                'list_key_groups',
                'list_origin_request_policies',
                'list_public_keys',
                'list_streaming_distributions'
            )
        ],
    )

    client = module.client('cloudfront', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudfront(client, module)

    if module.params['list_cache_policies']:
        module.exit_json(cache_policy_list=aws_cloudfornt_parser(paginate, _it, 'CachePolicyList', 'Items'))
    elif module.params['list_cloud_front_origin_access_identities']:
        module.exit_json(
            cloud_front_origin_access_identity_list=aws_cloudfornt_parser(
                paginate,
                _it,
                'CloudFrontOriginAccessIdentityList',
                'Items'
            )
        )
    elif module.params['list_field_level_encryption_configs']:
        module.exit_json(field_level_encryption_list=aws_cloudfornt_parser(paginate, _it, 'FieldLevelEncryptionList', 'Items'))
    elif module.params['list_field_level_encryption_profiles']:
        module.exit_json(field_level_encryption_profile_list=aws_cloudfornt_parser(paginate, _it, 'FieldLevelEncryptionProfileList', 'Items'))
    elif module.params['list_invalidations']:
        module.exit_json(invalidation_list=aws_cloudfornt_parser(paginate, _it, 'InvalidationList', 'Items'))
    elif module.params['list_key_groups']:
        module.exit_json(key_group_list=aws_cloudfornt_parser(paginate, _it, 'KeyGroupList', 'Items'))
    elif module.params['list_origin_request_policies']:
        module.exit_json(origin_request_policy_list=aws_cloudfornt_parser(paginate, _it, 'OriginRequestPolicyList', 'Items'))
    elif module.params['list_public_keys']:
        module.exit_json(public_key_list=aws_cloudfornt_parser(paginate, _it, 'PublicKeyList', 'Items'))
    elif module.params['list_streaming_distributions']:
        module.exit_json(streaming_distribution_list=aws_cloudfornt_parser(paginate, _it, 'StreamingDistributionList', 'Items'))
    else:
        module.exit_json(distribution_list=aws_cloudfornt_parser(paginate, _it, 'DistributionList', 'Items'))


if __name__ == '__main__':
    main()
