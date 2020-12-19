## Ansible Custom Library [![Build Status](https://travis-ci.com/116davinder/ansible-custom-libs.svg?branch=master)](https://travis-ci.com/116davinder/ansible-custom-libs)

## why this repository exists ?
Ansible community reviewers have too much ego
so I decided to host modules on my repository instead of ansible.

**Example:** https://116davinder.medium.com/story-of-unsuccessful-pr-to-open-source-project-da78db20613

## how to use these ansible custom library
```bash
git clone https://github.com/116davinder/ansible-custom-libs.git /tmp
export ANSIBLE_LIBRARY=/tmp/ansible-custom-libs
```

### List of Modules & Example Code

- [newrelic_deployment](test-code/newrelic_deployment.yml)
- [mapr_service](test-code/mapr_service.yml)
- [aws_ssm_parameter_store_v2](test-code/aws_ssm_parameter_store_v2.yml)
- [aws_sns_platform_info](test-code/aws_sns_platform_info.yml)
- [aws_sns_platform_endpoint_info](test-code/aws_sns_platform_endpoint_info.yml)
- [aws_sns_subscriptions_info](test-code/aws_sns_subscriptions_info.yml)
- [aws_sqs_queue_info](test-code/aws_sqs_queue_info.yml)
- [aws_eks_cluster_info](test-code/aws_eks_cluster_info.yml)
- [aws_athena_info](test-code/aws_athena_info.yml)

