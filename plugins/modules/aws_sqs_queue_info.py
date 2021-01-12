#!/usr/bin/python
# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = '''
---
module: aws_sqs_queue_info
version_added: 0.0.1
short_description: Get information about AWS SQS queues.
description:
  - List AWS SQS queues & there attributes.
  - U(https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_Operations.html)
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - boto3
options:
  queue_name_prefix:
    description:
      - filter queues with start name / initial characters.
      - Mutually Exclusive to queue_url.
      - Mutually Exclusive to dead_letter_source_queue.
    type: str
  queue_url:
    description:
      - amazon fqdn queue url.
      - U(https://queue.amazonaws.com/xxxx/test-sqs)
    type: str
  queue_attribute_name:
    description:
      - list of attributes to fetch only.
      - U(https://docs.aws.amazon.com/AWSSimpleQueueService/latest/APIReference/API_GetQueueAttributes.html)
    type: list
    default: ['All']
  dead_letter_source_queue:
    description:
      - If enabled, queue_url will be used as dead_letter_source_queue_url and
      - It will return all queue which are configured with queue_url as dead letter queue.
      - Mutually Exclusive to queue_attribute_name.
    type: bool
extends_documentation_fragment:
    - amazon.aws.aws
    - amazon.aws.ec2
'''

RETURN = '''
queue_urls:
    description: list of all `queue_name_prefix` or `dead_letter_source_queue` sqs urls
    type: list
    returned: when queue_name_prefix or dead_letter_source_queue or no module argument is defined and success
    sample: ["https://queue.amazonaws.com/xxxx/test-sqs"]
attributes:
    description: all or selected attributes of given sqs queue
    type: dict
    returned: when queue_attribute_name and queue_url is defined and success
    sample: {
        "approximate_number_of_messages": "0",
        "approximate_number_of_messages_delayed": "0",
        "approximate_number_of_messages_not_visible": "0",
        "created_timestamp": "1604324244",
        "delay_seconds": "0",
        "last_modified_timestamp": "1604326920",
        "maximum_message_size": "262144",
        "message_retention_period": "1209600",
        "policy": "{xxxxxxxx}",
        "queue_arn": "arn:aws:sqs:us-east-1:xxxxx:test-sqs",
        "receive_message_wait_time_seconds": "0",
        "redrive_policy": {
            "deadLetterTargetArn": "arn:aws:sqs:us-east-1:xxxxx:test-sqs-dead-queue",
            "maxReceiveCount": 100
        },
        "visibility_timeout": "900"
    }
'''

EXAMPLES = '''
- name: "get list of all sqs queues"
  sqs_queue_info:

- name: "get all sqs queues with prefix test"
  sqs_queue_info:
    queue_name_prefix: 'test'

- name: "get all attributes of given sqs queue"
  sqs_queue_info:
    queue_url: 'https://queue.amazonaws.com/xxxx/test-sqs'

- name: "get VisibilityTimeout & MaximumMessageSize attributes of given sqs queue"
  sqs_queue_info:
    queue_url: 'https://queue.amazonaws.com/xxxx/test-sqs'
    queue_attribute_name: ['VisibilityTimeout','MaximumMessageSize']

- name: "get sqs queues which have given dead letter queue"
  sqs_queue_info:
    queue_url: 'https://queue.amazonaws.com/xxxx/test-sqs'
    dead_letter_source_queue: true

'''

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry

try:
    from botocore.exceptions import BotoCoreError, ClientError, ParamValidationError
except ImportError:
    pass  # handled by AnsibleAWSModule


@AWSRetry.exponential_backoff()
def _sqs(module):
    try:
        client = module.client('sqs')
        if module.params['queue_url'] is not None:
            if module.params['dead_letter_source_queue'] is None:
                response = client.get_queue_attributes(
                    QueueUrl=module.params['queue_url'],
                    AttributeNames=module.params['queue_attribute_name']
                )
                module.exit_json(attributes=camel_dict_to_snake_dict(response['Attributes']))
            else:
                paginator = client.get_paginator('list_dead_letter_source_queues')
                iterator = paginator.paginate(
                    QueueUrl=module.params['queue_url']
                )
                for response in iterator:
                    module.exit_json(queue_urls=response['queueUrls'])
        else:
            paginator = client.get_paginator('list_queues')
            if module.params['queue_name_prefix'] is None:
                iterator = paginator.paginate()
            else:
                iterator = paginator.paginate(
                    QueueNamePrefix=module.params['queue_name_prefix']
                )
            for response in iterator:
                module.exit_json(queue_urls=response['QueueUrls'])

    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e)


def main():

    argument_spec = dict(
        queue_name_prefix=dict(required=False),
        queue_url=dict(required=False),
        queue_attribute_name=dict(required=False, default=['All'], type=list),
        dead_letter_source_queue=dict(required=False, type=bool)
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,

        required_if=(
            ('dead_letter_source_queue', True, ['queue_url']),
        ),
        mutually_exclusive=[
            ('queue_url', 'queue_name_prefix'),
            ('queue_name_prefix', 'dead_letter_source_queue'),
            ('queue_attribute_name', 'dead_letter_source_queue')
        ],
    )

    _sqs(module)


if __name__ == '__main__':
    main()
