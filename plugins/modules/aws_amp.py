#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_amp
short_description: Create / Update AWS Prometheus Service.
description:
  - Get Information about AWS Prometheus Service.
  - U(https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/amp.html)
version_added: 0.0.2
options:
  alias:
    description:
      - alias for aws amp service.
    required: true
    type: str
  client_token:
    description:
      - unique client token for aws amp service.
    required: true
    type: str
  state:
    description:
      - do you want to create/delete/update amp resource?
    required: false
    type: str
    choices: ['present', 'update', 'absent']
    default: 'present'
  workspace_id:
    description:
      - aws amp workspace unique id.
      - Used only when deleting/updating amp resources.
    required: false
    type: str
  new_alias:
    description:
      - new alias for amp resource.
      - Used only when updating amp resources.
    required: false
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
extends_documentation_fragment:
  - amazon.aws.ec2
  - amazon.aws.aws
requirements:
  - boto3>=1.16.43
  - botocore>=1.19.43
"""

EXAMPLES = """
- name: "create amp workspace"
  aws_amp:
    alias: '{{ alias }}'
    client_token: '{{ client_token }}'
    state: 'present'
  register: _create

- name: "update amp workspace alias"
  aws_amp:
    alias: '{{ alias }}'
    new_alias: 'new_alias'
    client_token: '{{ client_token }}'
    workspace_id: '{{ _create.workspace_id }}'
    state: 'update'

- name: "deleting amp workspace"
  aws_amp:
    alias: '{{ alias }}'
    client_token: '{{ client_token }}'
    workspace_id: '{{ _create.workspace_id }}'
    state: 'absent'
"""

RETURN = """
arn:
  description: arn of workspace.
  returned: when `state=present` and success
  type: str
  sample: arn:aws:aps:us-east-1:xxxxxx:workspace/ws-xxxxxxxxx-92fe-93cb8d9bff79
client_token:
  description: input `client_token` used for workspace.
  returned: when `state=present` and success
  type: str
  sample: 123456
status:
  description: status of workspace.
  returned: when `state=present` and success
  type: dict
  sample: {
    "status_code": "ACTIVE"
  }
workspace_id:
  description: id of workspace.
  returned: when `state=present` and success
  type: str
  sample: ws-xxxxxxxxx-92fe-93cb8d9bff79
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def main():
    argument_spec = dict(
        alias=dict(required=True),
        new_alias=dict(required=False),
        client_token=dict(required=True),
        state=dict(required=False, choices=['present', 'update', 'absent'], default='present'),
        workspace_id=dict(required=False)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
    )

    # remove below warning once amp service become GA
    module.warn("aws amp service is in open preview on 25-12-2020")

    amp = module.client('amp', retry_decorator=AWSRetry.exponential_backoff())

    if module.params['state'] == 'present':
        try:
            _changed = True
            _create = amp.create_workspace(
                alias=module.params['alias'],
                clientToken=module.params['client_token']
            )

            if _create['status']['statusCode'] == 'ACTIVE':
                _changed = False
            elif _create['status']['statusCode'] == 'CREATION_FAILED':
                module.fail_json(msg="creation failed")
            elif _create['status']['statusCode'] == 'DELETING':
                module.fail_json(
                    msg="previously created workspace is being deleted, Try again after one month or Use new client_token",
                    arn=_create['arn'],
                    status=camel_dict_to_snake_dict(_create['status']),
                    workspace_id=_create['workspaceId'],
                )

            module.exit_json(
                changed=_changed,
                arn=_create['arn'],
                status=camel_dict_to_snake_dict(_create['status']),
                workspace_id=_create['workspaceId'],
                client_token=module.params['client_token']
            )

        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e)
    elif module.params['state'] == 'update':
        try:
            if module.params['new_alias'] is None:
                module.fail_json(msg="missing argument new_alias")
            if module.params['workspace_id'] is None:
                module.fail_json(msg="missing argument workspace_id")
            if module.params['alias'] == module.params['new_alias']:
                module.fail_json(msg="new_alias can't be same as alias")

            try:
                _des = amp.describe_workspace(
                    workspaceId=module.params['workspace_id']
                )

                if _des['workspace']['status']['statusCode'] == 'UPDATING':
                    module.exit_json(msg="already updating workspace")
            except amp.exceptions.ResourceNotFoundException:
                module.fail_json(msg="workspace not found")

            amp.update_workspace_alias(
                alias=module.params['new_alias'],
                clientToken=module.params['client_token'],
                workspaceId=module.params['workspace_id']
            )

            module.exit_json(
                changed=True,
                msg="updating workspace alias to {}".format(module.params['new_alias'])
            )

        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e)
    else:
        try:
            if module.params['workspace_id'] is None:
                module.fail_json(msg="missing argument workspace_id")

            try:
                _des = amp.describe_workspace(
                    workspaceId=module.params['workspace_id']
                )

                if _des['workspace']['status']['statusCode'] == 'DELETING':
                    module.exit_json(msg="already deleting workspace")
            except amp.exceptions.ResourceNotFoundException:
                module.exit_json(msg="workspace not found")

            amp.delete_workspace(
                clientToken=module.params['client_token'],
                workspaceId=module.params['workspace_id']
            )

            module.exit_json(
                changed=True,
                msg="deleting workspace, actual data will be deleted within one month from now."
            )
        except (BotoCoreError, ClientError) as e:
            module.fail_json_aws(e)


if __name__ == '__main__':
    main()
