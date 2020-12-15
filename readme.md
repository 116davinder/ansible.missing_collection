## Ansible Custom Libs
* newrelic_deployment
* mapr_service
* aws_ssm_parameter_store
* sns_platform_info
* sns_platform_endpoint_info
* sns_subscriptions_info

## export ansible library path
export ANSIBLE_LIBRARY=`pwd`

## why required

```
To Support V2 Api of NewRelic for Recording of deployment.
```

* mapr_service
```
To manage mapr services using rest api.
```

### examples
```
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
  community.aws.aws_ssm_parameter_store:
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
```

