#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_config_info
short_description: Get Information about AWS Config.
description:
  - Get Information about AWS Config.
version_added: 1.4.0
options:
  id:
    description:
      - Id of Aws Config Application.
    required: false
    type: str
    aliases: ['application_id']
  list_configurations_profiles:
    description:
      - do you want to fetch configuration profiles for given application id.
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
- name: "get list of applications from aws config"
  aws_config_info:
  register: __all

- name: "get list of configurations profiles for given application id"
  aws_config_info:
    name: "{{ __all.applications[1] }}"
    list_configurations_profiles: true

"""

RETURN = """
applications:
  description: List of applications from aws config.
  returned: when no argument is defined and success
  type: list
  sample: [
    {
        'id': 'string',
        'name': 'string',
        'description': 'string'
    }
  ]
profiles:
  description: List of configurations profiles for given application id.
  returned: when I(list_configurations_profiles) and success
  type: list
  sample: [
      {
        'application_id': 'string',
        'id': 'string',
        'name': 'string',
        'location_uri': 'string',
        'validator_types': [
            'JSON_SCHEMA'|'LAMBDA',
        ]
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


@AWSRetry.exponential_backoff(retries=5, delay=5)
def _config(config, module):
    try:
        if module.params['list_configurations_profiles']:
            if config.can_paginate('list_configurations_profiles'):
                paginator = config.get_paginator('list_applications')
                iterator = paginator.paginate(
                    ApplicationId=module.params['id']
                )
                return iterator, True
            else:
                return config.list_applications(), False
        else:
            if config.can_paginate('list_applications'):
                paginator = config.get_paginator('list_applications')
                return paginator.paginate(), True
            else:
                return config.list_applications(), False

    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws config details')


def main():
    argument_spec = dict(
        id=dict(required=False, aliases=['application_id']),
        list_configurations_profiles=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('list_configurations_profiles', True, ['id']),
        ),
    )

    config = module.client('appconfig')
    __default_return = []

    _it, paginate = _config(config, module)
    if _it is not None:
        if module.params['list_configurations_profiles']:
            if paginate:
                for response in _it:
                    for _app in response['Items']:
                        __default_return.append(camel_dict_to_snake_dict(_app))
            else:
                for _app in _it['Items']:
                    __default_return.append(camel_dict_to_snake_dict(_app))
            module.exit_json(profiles=__default_return)
        else:
            if paginate:
                for response in _it:
                    for _app in response['Items']:
                        __default_return.append(camel_dict_to_snake_dict(_app))
            else:
                for _app in _it['Items']:
                    __default_return.append(camel_dict_to_snake_dict(_app))

            module.exit_json(applications=__default_return)


if __name__ == '__main__':
    main()
