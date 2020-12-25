## Ansible Missing Collection 
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/116davinder/ansible.missing_collection/CI%20Testing)
![Lines of code](https://img.shields.io/tokei/lines/github/116davinder/ansible.missing_collection)
![GitHub repo file count (custom path)](https://img.shields.io/github/directory-file-count/116davinder/ansible.missing_collection/plugins/modules)
![GitHub contributors](https://img.shields.io/github/contributors/116davinder/ansible.missing_collection)
![GitHub all releases](https://img.shields.io/github/downloads/116davinder/ansible.missing_collection/total)

It will host all new modules which doesn't exists in Official Ansible Collections and takes years to publish something new. Anyone who wan't to contribute, please feel free to create PR / Bug Report / Feature Request.

## Why this repository exists ?
Ansible Community reviewers takes too much time and have too hard restrictions.
So I decided to host modules on my repository instead of ansible.

**Examples:**
* https://116davinder.medium.com/story-of-unsuccessful-pr-to-open-source-project-da78db20613

## How to Install Ansible Missing Collection
```bash
$ ansible-galaxy collection install git+https://github.com/116davinder/ansible.missing_collection.git
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'community.missing_collection:0.0.0' to '/home/dpal/.ansible/collections/ansible_collections/community/missing_collection'
Created collection for community.missing_collection at /home/dpal/.ansible/collections/ansible_collections/community/missing_collection
community.missing_collection (0.0.0) was installed successfully

$ ansible-galaxy collection list
Collection                   Version
---------------------------- -------
community.missing_collection 0.0.0  

```

### List of Modules & Example Code

- [community.missing_collection.newrelic_deployment](tests/newrelic_deployment.yml)
- [community.missing_collection.mapr_service](tests/mapr_service.yml)
- [community.missing_collection.aws_ssm_parameter_store_v2](tests/aws_ssm_parameter_store_v2.yml)
- [community.missing_collection.aws_sns_platform_info](tests/aws_sns_platform_info.yml)
- [community.missing_collection.aws_sns_platform_endpoint_info](tests/aws_sns_platform_endpoint_info.yml)
- [community.missing_collection.aws_sns_subscriptions_info](tests/aws_sns_subscriptions_info.yml)
- [community.missing_collection.aws_sqs_queue_info](tests/aws_sqs_queue_info.yml)
- [community.missing_collection.aws_eks_cluster_info](tests/aws_eks_cluster_info.yml)
- [community.missing_collection.aws_athena_info](tests/aws_athena_info.yml)
- [community.missing_collection.aws_config_info](tests/aws_config_info.yml)
- [community.missing_collection.aws_backup_info](tests/aws_backup_info.yml)
- [community.missing_collection.aws_iam_access_analyzer_info](tests/aws_iam_access_analyzer_info.yml)
- [community.missing_collection.aws_amp](tests/aws_amp.yml)
- [community.missing_collection.aws_amp_info](tests/aws_amp_info.yml)

### License
None of these modules should be published to Official Ansible / Ansible-Collections without written confirmation from me( Davinder Pal ).
These Modules can be used/distributed in any project except Official Ansible / Ansible-Collections but only with my copyright statement 

`Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>`.

Any unknown cases, please better contact me ( Davinder Pal <dpsangwal@gmail.com> ).
