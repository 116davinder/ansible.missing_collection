#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: newrelic_deployment
author:
    - "Davinder Pal (@116davinder)"
version_added: 0.0.1
short_description: Notify newrelic about app deployments via v2 api.
description:
   - Notify newrelic about app deployments
        (U(https://docs.newrelic.com/docs/apm/new-relic-apm/maintenance/record-deployments)).
options:
  token:
    description:
      - API token, to place in the x-api-key header.
    required: true
    type: str
  app_name:
    description:
      - The value of C(app_name) in the C(newrelic.yml) file used by the application.
      - Exactly one of I(app_name) or I(application_id) is required.
    required: false
    type: str
  application_id:
    description:
      - The I(application_id), found in the URL when viewing the application in RPM.
      - See U(https://rpm.newrelic.com/api/explore/applications/list).
      - Exactly one of I(app_name) or I(application_id) is required.
    required: false
    type: str
  changelog:
    description:
      - A list of changes for this deployment.
    required: false
    type: str
  description:
    description:
      - Text annotation for the deployment - notes for you.
    required: false
    type: str
  revision:
    description:
      - A revision number (for example, git commit SHA).
    required: true
    type: str
  user:
    description:
      - The name of the user/process that triggered this deployment
    required: false
    type: str
'''

EXAMPLES = '''
- name:  Notify newrelic about an app deployment
  community.missing_collection.newrelic_deployment:
    token: XXXXXXXXX
    app_name: ansible_app
    user: ansible_deployment_user
    revision: '1.X'
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url
import json


# ===========================================
# Module execution.
#

def main():

    module = AnsibleModule(
        argument_spec=dict(
            token=dict(required=True, no_log=True),
            app_name=dict(required=False),
            application_id=dict(required=False),
            changelog=dict(required=False),
            description=dict(required=False),
            revision=dict(required=True),
            user=dict(required=False),
        ),
        required_one_of=[['app_name', 'application_id']],
        mutually_exclusive=[['app_name', 'application_id']],
    )

    if module.params['app_name']:
        data = 'filter[name]=' + str(module.params['app_name'])
        newrelic_api = 'https://api.newrelic.com/v2/applications.json'
        headers = {'x-api-key': module.params['token'],
                   'Content-Type': 'application/x-www-form-urlencoded'}
        (resp, info) = fetch_url(module,
                                 newrelic_api,
                                 headers=headers,
                                 data=data,
                                 method='GET')
        if info['status'] != 200:
            module.fail_json(msg="unable to get application list from newrelic: %s" % info['msg'])
        else:
            body = json.loads(resp.read())
        if body is None:
            module.fail_json(msg='No Data for applications')
        else:
            app_id = body['applications'][0]['id']
            if app_id is None:
                module.fail_json(msg="App not found in NewRelic Registerd Applications List")
    else:
        app_id = module.params['application_id']

    # Send the data to NewRelic
    url = 'https://api.newrelic.com/v2/applications/' + str(app_id) + '/deployments.json'
    data = {
        'deployment': {
            'revision': str(module.params['revision']),
            'changelog': str(module.params['changelog']),
            'description': str(module.params['description']),
            'user': str(module.params['user']), }
    }

    headers = {
        'x-api-key': module.params['token'],
        'Content-Type': 'application/json'
    }
    (_, info) = fetch_url(
        module,
        url,
        data=module.jsonify(data),
        headers=headers,
        method='POST'
    )
    if info['status'] == 201:
        module.exit_json(changed=True)
    else:
        module.fail_json(f'unable to update newrelic: {info["msg"]}')


if __name__ == '__main__':
    main()
