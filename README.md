## Ansible Missing Collection 
![GitHub Workflow Status](https://img.shields.io/github/workflow/status/116davinder/ansible.missing_collection/CI%20Testing)
![Lines of code](https://img.shields.io/tokei/lines/github/116davinder/ansible.missing_collection)
![GitHub contributors](https://img.shields.io/github/contributors/116davinder/ansible.missing_collection)
![GitHub all releases](https://img.shields.io/github/downloads/116davinder/ansible.missing_collection/total)

It will host all new modules which doesn't exists in Official Ansible Collections and takes years to publish something new. Anyone who wan't to contribute, please feel free to create PR / Bug Report / Feature Request.

## Why this repository exists ?
Ansible Community reviewers takes too much time and have too hard restrictions.
So I decided to host modules on my repository instead of ansible.

**Examples:**
* [Official Ansible PR: 1](https://github.com/ansible/ansible/pull/40029)
* [Official Ansible PR: 2](https://github.com/ansible-collections/community.general/pull/876)
* [Official Ansible PR: 3](https://github.com/ansible-collections/community.general/pull/1501)
* https://116davinder.medium.com/story-of-unsuccessful-pr-to-open-source-project-da78db20613

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

## How to Install Ansible Missing Collection
```bash
$ ansible-galaxy collection install git+https://github.com/116davinder/ansible.missing_collection.git
Starting galaxy collection install process
Process install dependency map
Starting collection install process
Installing 'community.missing_collection:0.0.2' to '/home/dpal/.ansible/collections/ansible_collections/community/missing_collection'
Created collection for community.missing_collection at /home/dpal/.ansible/collections/ansible_collections/community/missing_collection
community.missing_collection (0.0.2) was installed successfully

$ ansible-galaxy collection list
Collection                   Version
---------------------------- -------
community.missing_collection 0.0.2  

```

<!--start collection content-->
### Modules
Name | Description
--- | ---
[community.missing_collection.aws_amp](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_amp_module.rst)|Create / Update AWS Prometheus Service.
[community.missing_collection.aws_amp_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_amp_info_module.rst)|Get details about AWS Prometheus Service.
[community.missing_collection.aws_api_gateway_management_api](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_api_gateway_management_api_module.rst)|Manage Resources of Amazon API Gateway Management API.
[community.missing_collection.aws_api_gateway_management_api_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_api_gateway_management_api_info_module.rst)|Get details about Amazon API Gateway Management API.
[community.missing_collection.aws_api_gateway_v2_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_api_gateway_v2_info_module.rst)|Get details about AWS API Gateway V2 Service.
[community.missing_collection.aws_app_integrations_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_app_integrations_info_module.rst)|Get details about Amazon AppIntegrations Service.
[community.missing_collection.aws_appflow_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_appflow_info_module.rst)|Get details about AWS AppFlow Service.
[community.missing_collection.aws_application_auto_scaling_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_application_auto_scaling_info_module.rst)|Get details about AWS Application Auto Scaling.
[community.missing_collection.aws_application_insights_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_application_insights_info_module.rst)|Get details about Amazon CloudWatch Application Insights.
[community.missing_collection.aws_appmesh_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_appmesh_info_module.rst)|Get details about AWS App Mesh Service.
[community.missing_collection.aws_appstream_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_appstream_info_module.rst)|Get details about Amazon AppStream 2.0.
[community.missing_collection.aws_athena_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_athena_info_module.rst)|Get Information about AWS Athena.
[community.missing_collection.aws_auditmanager_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_auditmanager_info_module.rst)|Get details about AWS Audit Manager.
[community.missing_collection.aws_autoscaling_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_autoscaling_info_module.rst)|Get details about Amazon EC2 Auto Scaling.
[community.missing_collection.aws_autoscaling_plans_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_autoscaling_plans_info_module.rst)|Get details about AWS Auto Scaling Plans.
[community.missing_collection.aws_backup_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_backup_info_module.rst)|Get Information about AWS Backup.
[community.missing_collection.aws_batch_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_batch_info_module.rst)|Get details about AWS Batch.
[community.missing_collection.aws_cloud9_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloud9_info_module.rst)|Get details about AWS Cloud9 Environments.
[community.missing_collection.aws_cloudfront_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudfront_info_module.rst)|Get details about Amazon CloudFront.
[community.missing_collection.aws_cloudhsm_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudhsm_info_module.rst)|Get details about Amazon CloudHSM.
[community.missing_collection.aws_cloudhsm_v2_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudhsm_v2_info_module.rst)|Get details about Amazon CloudHSM V2.
[community.missing_collection.aws_cloudsearch_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudsearch_info_module.rst)|Get details about Amazon CloudSearch.
[community.missing_collection.aws_cloudtrail_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudtrail_info_module.rst)|Get Information about AWS Cloudtrail.
[community.missing_collection.aws_cloudwatch_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_cloudwatch_info_module.rst)|Get Information about AWS CloudWatch.
[community.missing_collection.aws_codeartifact_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_codeartifact_info_module.rst)|Get Information about AWS Code Artifact.
[community.missing_collection.aws_codebuild_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_codebuild_info_module.rst)|Get Information about AWS Code Build.
[community.missing_collection.aws_codecommit_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_codecommit_info_module.rst)|Get Information about AWS Code Commit.
[community.missing_collection.aws_codeguru_reviewer_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_codeguru_reviewer_info_module.rst)|Get Information about AWS Codeguru Reviewer.
[community.missing_collection.aws_codeguruprofiler_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_codeguruprofiler_info_module.rst)|Get Information about Amazon CodeGuru Profiler.
[community.missing_collection.aws_config_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_config_info_module.rst)|Get Information about AWS Config.
[community.missing_collection.aws_eks_cluster_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_eks_cluster_info_module.rst)|Get Information about AWS EKS Clusters.
[community.missing_collection.aws_iam_access_analyzer_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_iam_access_analyzer_info_module.rst)|Get Information about AWS IAM Access Analyzer.
[community.missing_collection.aws_sns_platform_endpoint_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_sns_platform_endpoint_info_module.rst)|Get Information about AWS SNS Platforms.
[community.missing_collection.aws_sns_platform_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_sns_platform_info_module.rst)|Get Information about AWS SNS Platforms.
[community.missing_collection.aws_sns_subscriptions_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_sns_subscriptions_info_module.rst)|Get Information about AWS SNS Subscriptions.
[community.missing_collection.aws_sqs_queue_info](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_sqs_queue_info_module.rst)|Get information about AWS SQS queues.
[community.missing_collection.aws_ssm_parameter_store](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.aws_ssm_parameter_store_module.rst)|Manage key-value pairs in aws parameter store.
[community.missing_collection.mapr_service](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.mapr_service_module.rst)|Manage MapR Services by rest api.
[community.missing_collection.newrelic_deployment](https://github.com/116davinder/ansible.missing_collection/blob/master/docs/community.missing_collection.newrelic_deployment_module.rst)|Notify newrelic about app deployments via v2 api.

<!--end collection content-->

### Install ansible automatic doc creation tool ?
```bash
$ pip3 install git+https://github.com/ansible-network/collection_prep.git
```

### Generate docs from ansible tool ?
```bash
$ collection_prep_add_docs -p . -b master
INFO      Setting collection name to community.missing_collection
INFO      Setting GitHub repository url to https://github.com/116davinder/ansible.missing_collection
INFO      Purging content from directory /home/dpal/python-projects/ansible.missing_collection/docs
INFO      Making docs directory /home/dpal/python-projects/ansible.missing_collection/docs
INFO      Process content in /home/dpal/python-projects/ansible.missing_collection/plugins/modules
INFO      Processing /home/dpal/python-projects/ansible.missing_collection/plugins/modules/aws_amp_info.py
..............
INFO      Processing 'modules' for README
ERROR     README.md not found in ./ansible.missing_collection
ERROR     README.md not updated
```
