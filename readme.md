## Ansible Custom Library
* newrelic_deployment
* mapr_service
* aws_ssm_parameter_store_v2
* sns_platform_info
* sns_platform_endpoint_info
* sns_subscriptions_info
* sqs_queue_info

## export ansible library path
export ANSIBLE_LIBRARY=`pwd`

### examples
```yaml
- newrelic_deployment:
    token: XXXXXXXXX
    app_name: ansibleApp
    user: ansible deployment user
    revision: '1.X'

- mapr_service:
    username: mapr
    password: mapr
    service_name: nfs
    mcs_url: demo.mapr.com
    mcs_port: 8443
    state: restart
    validate_certs: false

- name: Create or update key/value pair in aws parameter store with tier
  aws_ssm_parameter_store:
    name: "Hello"
    description: "This is your first key"
    value: "World"
    tier: "Advanced"

- name: Get list of SNS platform applications but enabled only.
  sns_platform_info:
    enabled: 'true'

- name: Get list of Endpoints SNS platform Endpoints but enabled only.
  sns_platform_endpoint_info:
    arn: arn:aws:sns:us-east-1:xxxxx:app/APNS/xxxxx-platform-app
    enabled: 'true'

- name: Get list of SNS Subscriptions for given topic.
  sns_subscriptions_info:
    arn: 'arn:aws:sns:us-east-1:xxx:test'

- name: "get list of all sqs queues"
  sqs_queue_info:

- name: "get all sqs queues with prefix tools-preprod"
  sqs_queue_info:
    queue_name_prefix: 'tools-preprod'
  register: __tools

- name: "get all attributes of given sqs queue"
  sqs_queue_info:
    queue_url: '{{ __tools.queue_urls[0] }}'

- name: "get VisibilityTimeout & MaximumMessageSize arttributes of given sqs queue"
  sqs_queue_info:
    queue_url: '{{ __tools.queue_urls[0] }}'
    queue_attribute_name: ['VisibilityTimeout','MaximumMessageSize']

- name: "get sqs queues which have given dead letter queue"
  sqs_queue_info:
    queue_url: '{{ __tools.queue_urls[1] }}'
    dead_letter_source_queue: true
```

