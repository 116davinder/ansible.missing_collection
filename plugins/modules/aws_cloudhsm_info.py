#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudhsm_info
short_description: Get details about Amazon CloudHSM.
description:
  - Get Information about Amazon CloudHSM.
  - U(https://docs.aws.amazon.com/cloudhsm/classic/APIReference/API_Operations.html)
version_added: 0.0.3
options:
  arn:
    description:
      - can be arn of hsm?
      - can be arn of hapg?
      - can be luna client certificate arn?
    required: false
    type: str
  certificate_fingerprint:
    description:
      - luna client certificate fingerprint?
    required: false
    type: str
  list_hsms:
    description:
      - do you want to list all hsms?
    required: false
    type: bool
  list_hapgs:
    description:
      - do you want to list all high-availability partition group?
    required: false
    type: bool
  list_luna_clients:
    description:
      - do you want to list all hsms clients?
    required: false
    type: bool
  describe_hapg:
    description:
      - do you want to describe high-availability partition group of I(arn)?
    required: false
    type: bool
  describe_hsm:
    description:
      - do you want to describe hsm of I(arn)?
    required: false
    type: bool
  describe_luna_client:
    description:
      - do you want to describe luna client of I(arn) and I(certificate_fingerprint)?
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
- name: "list available zones of cloudhsm"
  aws_cloudhsm_info:
    register: _az

- name: "Retrieves the identifiers of all of the HSMs provisioned"
  aws_cloudhsm_info:
    list_hsms: true

- name: "Lists the high-availability partition groups"
  aws_cloudhsm_info:
    list_hapgs: true

- name: "Lists all of the luna clients."
  aws_cloudhsm_info:
    list_luna_clients: true

- name: "Retrieves information about a high-availability partition group."
  aws_cloudhsm_info:
    describe_hapg: true
    arn: 'hapg_arn'

- name: "Retrieves information about an HSM."
  aws_cloudhsm_info:
    describe_hsm: true
    arn: 'cloud_hsm_arn'
    serial_number: '122344545'

- name: "Retrieves information about an HSM client."
  aws_cloudhsm_info:
    describe_luna_client: true
    arn: 'client_cert_arn'
    certificate_fingerprint: 'certificate_fingerprint'
"""

RETURN = """
az_list:
  description: Lists the Availability Zones that have available AWS CloudHSM capacity.
  returned: when no argument and success
  type: list
  sample: [ 'string', ]
hsm_list:
  description: Retrieves the identifiers of all of the HSMs provisioned.
  returned: when `list_hsms` is defined and success
  type: list
  sample: [ 'string', ]
hapg_list:
  description: Lists the high-availability partition groups.
  returned: when `list_hapgs` is defined and success
  type: list
  sample: [ 'string', ]
luna_client_list:
  description: Lists all of the Luna clients.
  returned: when `list_luna_clients` is defined and success
  type: list
  sample: [ 'string', ]
hapg:
  description: Retrieves information about a high-availability partition group.
  returned: when `describe_hapg` and `arn` are defined and success
  type: dict
  sample: {
    'hapg_arn': 'string',
    'hapg_serial': 'string',
    'hsms_last_acction_failed': [],
    'hsms_pending_deletion': [],
    'hsms_pending_registration': [],
    'label': 'string',
    'last_modified_timestamp': 'string',
    'partition_serial_list': [],
    'state': 'READY'
  }
hsm:
  description: Retrieves information about an HSM.
  returned: when `describe_hsm` is defined and success
  type: dict
  sample: {
    'hsm_arn': 'string',
    'status': 'PENDING',
    'status_details': 'string',
    'availability_zone': 'string',
    'eni_id': 'string',
    'eni_ip': 'string',
    'subscription_type': 'PRODUCTION',
    'subscription_start_date': 'string',
    'subscription_end_date': 'string',
    'vpc_id': 'string',
    'subnet_id': 'string',
    'iam_role_arn': 'string',
    'serial_number': 'string',
    'vendor_name': 'string',
    'hsm_type': 'string',
    'software_version': 'string',
    'ssh_public_key': 'string',
    'ssh_key_last_updated': 'string',
    'server_cert_uri': 'string',
    'server_cert_last_updated': 'string',
    'partitions': []
  }
luna_client:
  description: Retrieves information about an HSM client.
  returned: when `describe_luna_client` and `arn` and `certificate_fingerprint` are defined and success
  type: dict
  sample: {
    'client_arn': 'string',
    'certificate': 'string',
    'certificate_fingerprint': 'string',
    'last_modified_timestamp': 'string',
    'label': 'string'
  }
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry


def aws_response_list_parser(paginate: bool, iterator, resource_field: str) -> list:
    _return = []
    if iterator is not None:
        if paginate:
            for response in iterator:
                for _app in response[resource_field]:
                    _return.append(camel_dict_to_snake_dict(_app))
        else:
            for _app in iterator[resource_field]:
                _return.append(camel_dict_to_snake_dict(_app))
    return _return


def _cloudhsm(client, module):
    try:
        if module.params['list_hsms']:
            if client.can_paginate('list_hsms'):
                paginator = client.get_paginator('list_hsms')
                return paginator.paginate(), True
            else:
                return client.list_hsms(), False
        elif module.params['list_hapgs']:
            if client.can_paginate('list_hapgs'):
                paginator = client.get_paginator('list_hapgs')
                return paginator.paginate(), True
            else:
                return client.list_hapgs(), False
        elif module.params['list_luna_clients']:
            if client.can_paginate('list_luna_clients'):
                paginator = client.get_paginator('list_luna_clients')
                return paginator.paginate(), True
            else:
                return client.list_luna_clients(), False
        elif module.params['describe_hapg']:
            return client.describe_hapg(
                HapgArn=module.params['arn']
            ), False
        elif module.params['describe_hsm']:
            return client.describe_hsm(
                HsmArn=module.params['arn'],
            ), False
        elif module.params['describe_luna_client']:
            return client.describe_luna_client(
                ClientArn=module.params['arn'],
                CertificateFingerprint=module.params['certificate_fingerprint'],
            ), False
        else:
            if client.can_paginate('list_available_zones'):
                paginator = client.get_paginator('list_available_zones')
                return paginator.paginate(), True
            else:
                return client.list_available_zones(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudhsm details')


def main():
    argument_spec = dict(
        arn=dict(required=False),
        certificate_fingerprint=dict(required=False),
        list_hsms=dict(required=False, type=bool),
        list_hapgs=dict(required=False, type=bool),
        list_luna_clients=dict(required=False, type=bool),
        describe_hapg=dict(required=False, type=bool),
        describe_hsm=dict(required=False, type=bool),
        describe_luna_client=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_hapg', True, ['arn']),
            ('describe_hsm', True, ['arn']),
            ('describe_luna_client', True, ['arn', 'certificate_fingerprint']),
        ],
        mutually_exclusive=[
            (
                'list_hsms',
                'list_hapgs',
                'list_luna_clients',
                'describe_hapg',
                'describe_hsm',
                'describe_luna_client',
            ),
        ],
    )

    client = module.client('cloudhsm', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudhsm(client, module)

    if module.params['list_hsms']:
        module.exit_json(hsm_list=aws_response_list_parser(paginate, _it, 'HsmList'))
    elif module.params['list_hapgs']:
        module.exit_json(hapg_list=aws_response_list_parser(paginate, _it, 'HapgList'))
    elif module.params['list_luna_clients']:
        module.exit_json(luna_client_list=aws_response_list_parser(paginate, _it, 'ClientList'))
    elif module.params['describe_hapg']:
        module.exit_json(hapg=camel_dict_to_snake_dict(_it))
    elif module.params['describe_hsm']:
        module.exit_json(hsm=camel_dict_to_snake_dict(_it))
    elif module.params['describe_luna_client']:
        module.exit_json(luna_client=camel_dict_to_snake_dict(_it))
    else:
        module.exit_json(az_list=aws_response_list_parser(paginate, _it, 'AZList'))


if __name__ == '__main__':
    main()
