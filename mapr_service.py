#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2018 Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.1', 'status': ['preview'],
                    'supported_by': 'individual'}

DOCUMENTATION = \
    '''
---
module: mapr_service
version_added: "0.1"
author: "Davinder Pal (@116davinder)"
short_description: Manage MapR Services by rest api.
description:
   - Manage MapR Services
        (https://mapr.com/docs/52/ReferenceGuide/REST-API-Syntax.html)
options:
  app_name:
    description:
      - (one of app_name or application_id are required)
        The value of app_name in the newrelic.yml file used by the application
    required: false
  application_id:
    description:
      - (one of app_name or application_id are required)
        (see https://rpm.newrelic.com/api/explore/applications/list)
    required: false
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated.
        This should only be used for personal self-signed certificates.
    required: false
    default: 'yes'
    type: bool
    version_added: 2.6.x
'''

EXAMPLES = \
    '''
- newrelic_deployment:
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
            username=dict(required=True),
            password=dict(required=True, no_log=False),
            service_name=dict(required=True),
            mcs_url=dict(required=True),
            mcs_port=dict(default='8443',required=False),
            state=dict(required=True),
            validate_certs=dict(default='False', type='bool'),
        )
    )

    mapr_default_service_state = ['start','stop','restart']

    def get_current_hostname():
        cmd = module.get_bin_path('hostname', True)
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            module.fail_json(msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return out.strip()

    if (module.params['username'] or module.params['password']
            or module.params['service_name'] or module.params['mcs_url']
            or module.params['state'] ):
        module.fail_json(msg="all values should to be defined except mcs_port/validate_certs")
    elif module.params['state'] not in mapr_default_service_state:
        module.fail_json(msg="state should be start/stop/restart only")
    else:
        host = get_current_hostname()
        url_parameters = "?action=" + module.params['state'] + "&nodes=" + str(host) + "&name=" + module.params['service_name']

#https://mapr.local:8443/rest/node/services?action=start&nodes=mapr.local&name=nfs
        complete_url = "https://" + module.params['mcs_url'] + module.params['mcs_port'] + url_parameters
        headers = "'Content-Type': 'application/json'"
        (resp, info) = fetch_url(module,
                                 complete_url,
                                 headers=headers,
                                 method='GET')
        body = resp.read()
        if info['status'] != 200:
            module.fail_json(msg="unable to reach mcs url " + module.params['mcs_url'])
        elif body.status != "OK":
            module.fail_json(msg="unable to + " + module.params['state'] + ": %s" % body.errors)
        else:
            module.exit_json(changed=True)

if __name__ == '__main__':
    main()