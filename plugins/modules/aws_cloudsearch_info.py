#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2020, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: aws_cloudsearch_info
short_description: Get details about Amazon CloudSearch.
description:
  - Get Information about Amazon CloudSearch.
  - U(https://docs.aws.amazon.com/cloudsearch/latest/developerguide/API_Operations.html)
version_added: 0.0.3
options:
  domain_name:
    description:
      - name of cloudsearch domain.
    required: false
    type: str
  domain_names:
    description:
      - name of cloudsearch domains.
    required: false
    type: list
  expression_names:
    description:
      - name of cloudsearch domain expression names.
    required: false
    type: list
  field_names:
    description:
      - name of cloudsearch domain index field names.
    required: false
    type: list
  suggester_names:
    description:
      - name of cloudsearch domain suggester names.
    required: false
    type: list
  analysis_scheme_names:
    description:
      - name of cloudsearch domain analysis scheme names.
    required: false
    type: list
  describe_clusters:
    description:
      - do you want to describe CloudSearch clusters given I(cluster_ids)?
    required: false
    type: bool
  deployed:
    description:
      - do you want to describe deployed resources?
      - can be used all types of describe options except: I(describe_scaling_parameters) and I(describe_domains)
    required: false
    type: bool
  describe_analysis_schemes:
    description:
      - do you want to describe CloudSearch analysis scheme names for given I(domain_name) and I(analysis_scheme_names)?
    required: false
    type: bool
  describe_availability_options:
    description:
      - do you want to describe CloudSearch avialability options for given I(domain_name)?
    required: false
    type: bool
  describe_domain_endpoint_options:
    description:
      - do you want to describe CloudSearch endpoint options for given I(domain_name)?
    required: false
    type: bool
  describe_domains:
    description:
      - do you want to describe CloudSearch domains for given I(domain_names)?
    required: false
    type: bool
  describe_expressions:
    description:
      - do you want to describe CloudSearch domain expressions for given I(domain_name) and I(expression_names)?
    required: false
    type: bool
  describe_index_fields:
    description:
      - do you want to describe CloudSearch domain index fields for given I(domain_name) and I(field_names)?
    required: false
    type: bool
  describe_scaling_parameters:
    description:
      - do you want to describe CloudSearch domain scaling parameters for given I(domain_name)?
    required: false
    type: bool
  describe_service_access_policies:
    description:
      - do you want to describe CloudSearch domain access policies for given I(domain_name)?
    required: false
    type: bool
  describe_suggesters:
    description:
      - do you want to describe CloudSearch domain suggester for given I(domain_name) and I(suggester_names)?
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
- name: "list cloudsearch domains"
  aws_cloudsearch_info:

- name: "describe test analysis schemas"
  aws_cloudsearch_info:
    describe_analysis_schemes: true
    domain_name: "test"
    analysis_scheme_names: ['test']

- name: "describe availability options"
  aws_cloudsearch_info:
    describe_availability_options: true
    domain_name: "test"

- name: "describe domain endpoint options"
  aws_cloudsearch_info:
    describe_domain_endpoint_options: true
    domain_name: "test"

- name: "describe domains"
  aws_cloudsearch_info:
    describe_domains: true
    domain_names: ["test"]

- name: "describe expressions"
  aws_cloudsearch_info:
    describe_expressions: true
    domain_name: "test"
    expression_names: ['test']

- name: "describe index fields"
  aws_cloudsearch_info:
    describe_index_fields: true
    domain_name: "test"
    field_names: ['rank']

- name: "describe scaling parameters"
  aws_cloudsearch_info:
    describe_scaling_parameters: true
    domain_name: "test"

- name: "describe service access policies"
  aws_cloudsearch_info:
    describe_service_access_policies: true
    domain_name: "test"

- name: "describe suggesters"
  aws_cloudsearch_info:
    describe_suggesters: true
    domain_name: "test"
    suggester_names: "test"
"""

RETURN = """
domain_names:
  description: List of CloudSearch Domains.
  returned: when no argument and success
  type: dict
  sample: { 'string': 'string' }
analysis_schemes:
  description: Description of CloudSearch Analysis Schemas.
  returned: when `describe_analysis_schemes` and `domain_name` and `analysis_scheme_names` are defined and success
  type: list
  sample: [
      {
          'options': {
              'analysis_scheme_name': 'string',
              'analysis_scheme_language': 'ar',
              'analysis_options': {}
          },
          'status': {}
      },
  ]
availability_options:
  description: Description of CloudSearch Domain availability options.
  returned: when `describe_availability_options` and `domain_name` are defined and success
  type: dict
  sample: {
      'options': True,
      'status': {
          'creation_date': datetime(2015, 1, 1),
          'update_date': datetime(2016, 6, 6),
          'update_version': 123,
          'state': 'RequiresIndexDocuments',
          'pending_deletion': True
      }
  }
domain_endpoint_options:
  description: Description of CloudSearch domain endpoint options.
  returned: when `describe_domain_endpoint_options` and `domain_name` are defined and success
  type: dict
  sample: {
      'options': {
          'enforce_https': True,
          'tls_security_policy': 'Policy-Min-TLS-1-0-2019-07'
      },
      'status': {
          'creation_date': datetime(2015, 1, 1),
          'update_date': datetime(2016, 6, 6),
          'update_version': 123,
          'state': 'RequiresIndexDocuments',
          'pending_deletion': True
      }
  }
domain_status_list:
  description: Description of CloudSearch domain status list.
  returned: when `describe_domains` and `domain_names` are defined and success
  type: list
  sample: [
      {
          'domain_id': 'string',
          'domain_name': 'string',
          'arn': 'string',
          'created': True,
          'deleted': False,
          'doc_service': {
              'endpoint': 'string'
          },
          'search_service': {
              'endpoint': 'string'
          },
          'requires_index_documents': True,
          'processing': True,
          'search_nstance_type': 'string',
          'search_partition_count': 123,
          'search_instance_count': 123,
          'limits': {
              'maximum_replication_count': 123,
              'maximum_partition_count': 123
          }
      },
  ]
expressions:
  description: Description of CloudSearch domain expressions.
  returned: when `describe_expressions` and `domain_name` and `expression_names` are defined and success
  type: list
  sample: [
      {
          'options': {
              'expression_name': 'string',
              'expression_value': 'string'
          },
          'status': {
              'creation_date': datetime(2015, 1, 1),
              'update_date': datetime(2016, 6, 6),
              'update_version': 123,
              'state': 'RequiresIndexDocuments',
              'pending_deletion': True
          }
      },
  ]
index_fields:
  description: Description of CloudSearch index fields.
  returned: when `describe_index_fields` and `domain_name` and `field_names` are defined and success
  type: list
  sample: [
      {
          'options': {
              'index_field_name': 'string',
              'index_field_type': 'int',
              'int_options': {},
              'double_options': {},
              'literal_options': {},
              'text_options': {},
              'date_options': {},
              'lat_lon_options': {},
              'int_array_options': {},
              'double_array_options': {},
              'literal_array_options': {},
              'text_array_options': {},
              'date_array_options': {}
          },
          'status': {
              'creation_date': datetime(2015, 1, 1),
              'update_date': datetime(2016, 6, 6),
              'update_version': 123,
              'state': 'RequiresIndexDocuments',
              'pending_deletion': True
          }
      },
  ]
scaling_parameters:
  description: Description of CloudSearch scaling parameters.
  returned: when `describe_scaling_parameters` and `domain_name` are defined and success
  type: dict
  sample: {
      'options': {
          'desired_instance_type': 'search.m1.small',
          'desired_replication_count': 123,
          'desired_partition_count': 123
      },
      'status': {
          'creation_date': datetime(2015, 1, 1),
          'update_date': datetime(2016, 6, 6),
          'update_version': 123,
          'state': 'RequiresIndexDocuments',
          'pending_deletion': True
      }
  }
access_policies:
  description: Description of CloudSearch domain access policies.
  returned: when `describe_service_access_policies` and `domain_name` are defined and success
  type: dict
  sample: {
      'options': 'string',
      'status': {
          'creation_date': datetime(2015, 1, 1),
          'update_date': datetime(2016, 6, 6),
          'update_version': 123,
          'state': 'RequiresIndexDocuments',
          'pending_deletion': True
      }
  }
suggesters:
  description: Describe of CloudSearch domain suggesters.
  returned: when `describe_suggesters` and `domain_name` and `suggester_names` are defined and success
  type: list
  sample: [
      {
          'options': {
              'suggester_name': 'string',
              'document_suggester_options': {
                  'source_field': 'string',
                  'fuzzy_matching': 'none',
                  'sort_expression': 'string'
              }
          },
          'status': {
              'creation_date': datetime(2015, 1, 1),
              'update_date': datetime(2016, 6, 6),
              'update_version': 123,
              'state': 'RequiresIndexDocuments',
              'pending_deletion': True
          }
      },
  ]
"""

try:
    from botocore.exceptions import BotoCoreError, ClientError
except ImportError:
    pass    # Handled by AnsibleAWSModule

from ansible_collections.amazon.aws.plugins.module_utils.core import AnsibleAWSModule
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import camel_dict_to_snake_dict
from ansible_collections.amazon.aws.plugins.module_utils.ec2 import AWSRetry
from ansible_collections.community.missing_collection.plugins.module_utils.aws_response_parser import aws_response_list_parser


def _cloudsearch(client, module):
    try:
        if module.params['describe_analysis_schemes']:
            if client.can_paginate('describe_analysis_schemes'):
                paginator = client.get_paginator('describe_analysis_schemes')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    AnalysisSchemeNames=module.params['analysis_scheme_names'],
                    Deployed=module.params['deployed'],
                ), True
            else:
                return client.describe_analysis_schemes(
                    DomainName=module.params['domain_name'],
                    AnalysisSchemeNames=module.params['analysis_scheme_names'],
                    Deployed=module.params['deployed'],
                ), False
        elif module.params['describe_availability_options']:
            if client.can_paginate('describe_availability_options'):
                paginator = client.get_paginator('describe_availability_options')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), True
            else:
                return client.describe_availability_options(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), False
        elif module.params['describe_domain_endpoint_options']:
            if client.can_paginate('describe_domain_endpoint_options'):
                paginator = client.get_paginator('describe_domain_endpoint_options')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), True
            else:
                return client.describe_domain_endpoint_options(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), False
        elif module.params['describe_domains']:
            if client.can_paginate('describe_domains'):
                paginator = client.get_paginator('describe_domains')
                return paginator.paginate(
                    DomainNames=module.params['domain_names'],
                ), True
            else:
                return client.describe_domains(
                    DomainNames=module.params['domain_names'],
                ), False
        elif module.params['describe_expressions']:
            if client.can_paginate('describe_expressions'):
                paginator = client.get_paginator('describe_expressions')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    ExpressionNames=module.params['expression_names'],
                ), True
            else:
                return client.describe_expressions(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    ExpressionNames=module.params['expression_names'],
                ), False
        elif module.params['describe_index_fields']:
            if client.can_paginate('describe_index_fields'):
                paginator = client.get_paginator('describe_index_fields')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    FieldNames=module.params['field_names'],
                ), True
            else:
                return client.describe_index_fields(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    FieldNames=module.params['field_names'],
                ), False
        elif module.params['describe_scaling_parameters']:
            if client.can_paginate('describe_scaling_parameters'):
                paginator = client.get_paginator('describe_scaling_parameters')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                ), True
            else:
                return client.describe_scaling_parameters(
                    DomainName=module.params['domain_name'],
                ), False
        elif module.params['describe_service_access_policies']:
            if client.can_paginate('describe_service_access_policies'):
                paginator = client.get_paginator('describe_service_access_policies')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), True
            else:
                return client.describe_service_access_policies(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                ), False
        elif module.params['describe_suggesters']:
            if client.can_paginate('describe_suggesters'):
                paginator = client.get_paginator('describe_suggesters')
                return paginator.paginate(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    SuggesterNames=module.params['suggester_names'],
                ), True
            else:
                return client.describe_suggesters(
                    DomainName=module.params['domain_name'],
                    Deployed=module.params['deployed'],
                    SuggesterNames=module.params['suggester_names'],
                ), False
        else:
            if client.can_paginate('list_domain_names'):
                paginator = client.get_paginator('list_domain_names')
                return paginator.paginate(), True
            else:
                return client.list_domain_names(), False
    except (BotoCoreError, ClientError) as e:
        module.fail_json_aws(e, msg='Failed to fetch aws cloudsearch details')


def main():
    argument_spec = dict(
        domain_name=dict(required=False),
        domain_names=dict(required=False, type=list),
        expression_names=dict(required=False, type=list),
        field_names=dict(required=False, type=list),
        suggester_names=dict(required=False, type=list),
        analysis_scheme_names=dict(required=False, type=list),
        deployed=dict(required=False, type=bool, default=False),
        describe_analysis_schemes=dict(required=False, type=bool),
        describe_availability_options=dict(required=False, type=bool),
        describe_domain_endpoint_options=dict(required=False, type=bool),
        describe_domains=dict(required=False, type=bool),
        describe_expressions=dict(required=False, type=bool),
        describe_index_fields=dict(required=False, type=bool),
        describe_scaling_parameters=dict(required=False, type=bool),
        describe_service_access_policies=dict(required=False, type=bool),
        describe_suggesters=dict(required=False, type=bool),
    )

    module = AnsibleAWSModule(
        argument_spec=argument_spec,
        required_if=[
            ('describe_analysis_schemes', True, ['domain_name', 'analysis_scheme_names']),
            ('describe_availability_options', True, ['domain_name']),
            ('describe_domain_endpoint_options', True, ['domain_name']),
            ('describe_domains', True, ['domain_names']),
            ('describe_expressions', True, ['domain_name', 'expression_names']),
            ('describe_index_fields', True, ['domain_name', 'field_names']),
            ('describe_scaling_parameters', True, ['domain_name']),
            ('describe_service_access_policies', True, ['domain_name']),
            ('describe_suggesters', True, ['domain_name', 'suggester_names']),
        ],
        mutually_exclusive=[
            (
                'describe_analysis_schemes',
                'describe_availability_options',
                'describe_domain_endpoint_options',
                'describe_domains',
                'describe_expressions',
                'describe_index_fields',
                'describe_scaling_parameters',
                'describe_service_access_policies',
                'describe_suggesters',
            ),
        ],
    )

    client = module.client('cloudsearch', retry_decorator=AWSRetry.exponential_backoff())
    _it, paginate = _cloudsearch(client, module)

    if module.params['describe_analysis_schemes']:
        module.exit_json(analysis_schemes=aws_response_list_parser(paginate, _it, 'AnalysisSchemes'))
    elif module.params['describe_availability_options']:
        module.exit_json(availability_options=camel_dict_to_snake_dict(_it['AvailabilityOptions']))
    elif module.params['describe_domain_endpoint_options']:
        module.exit_json(domain_endpoint_options=camel_dict_to_snake_dict(_it['DomainEndpointOptions']))
    elif module.params['describe_domains']:
        module.exit_json(domain_status_list=aws_response_list_parser(paginate, _it, 'DomainStatusList'))
    elif module.params['describe_expressions']:
        module.exit_json(expressions=aws_response_list_parser(paginate, _it, 'Expressions'))
    elif module.params['describe_index_fields']:
        module.exit_json(index_fields=aws_response_list_parser(paginate, _it, 'IndexFields'))
    elif module.params['describe_scaling_parameters']:
        module.exit_json(scaling_parameters=camel_dict_to_snake_dict(_it['ScalingParameters']))
    elif module.params['describe_service_access_policies']:
        module.exit_json(access_policies=camel_dict_to_snake_dict(_it['AccessPolicies']))
    elif module.params['describe_suggesters']:
        module.exit_json(suggesters=aws_response_list_parser(paginate, _it, 'Suggesters'))
    else:
        module.exit_json(domain_names=camel_dict_to_snake_dict(_it['DomainNames']))


if __name__ == '__main__':
    main()
