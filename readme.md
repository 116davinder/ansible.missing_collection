## Ansible Custom Library
* newrelic_deployment
* mapr_service
* aws_ssm_parameter_store_v2
* sns_platform_info
* sns_platform_endpoint_info
* sns_subscriptions_info
* sqs_queue_info
* aws_eks_cluster_info

## how to use these ansible custom library
```bash
git clone https://github.com/116davinder/ansible-custom-libs.git /tmp
export ANSIBLE_LIBRARY=/tmp/ansible-custom-libs
```

### Examples
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
  aws_ssm_parameter_store_v2:
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

- name: "get list of eks clusters"
  aws_eks_cluster_info:
  register: __all

- name: "get fargate profiles for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_fargate_profiles: true

- name: "get nodegroups for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_nodegroups: true

- name: "get list of addons for given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    list_addons: true

- name: "get details about given cluster"
  aws_eks_cluster_info:
    name: "{{ __all.clusters[1] }}"
    describe_cluster: true
```

