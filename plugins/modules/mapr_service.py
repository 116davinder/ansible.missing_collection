#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2018 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: mapr_service
version_added: 0.0.1
author: "Davinder Pal (@116davinder)"
short_description: Manage MapR Services by rest api.
description:
   - Manage MapR Services
        (https://mapr.com/docs/52/ReferenceGuide/REST-API-Syntax.html)
options:
  username:
    description:
      - username for MapR MCS
    required: true
    type: string
  password:
    description:
      - password for MapR MCS
    required: true
    type: string
  service_name:
    description:
      - name of service on which you want to do action
      - example nfs,fileserver,cldb etc.
    required: true
    type: string
  mcs_url:
    description:
      - Mapr MCS Web Address like demo.mapr.com
      - Note: It should not include port number for MCS
    required: true
    type: string
  mcs_port:
    description:
      - Mapr MCS Port
    required: false
    default: 8443
    type: string
  state:
    description:
      - state of application like start/stop/restart
    required: true
    type: string
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated.
        This should only be used for personal self-signed certificates.
    required: false
    default: 'yes'
    type: bool
    version_added: 2.6.x
'''

EXAMPLES = '''
- community.missing_collection.mapr_service:
    username: mapr
    password: mapr
    service_name: nfs
    mcs_url: demo.mapr.com
    mcs_port: 8443
    state: restart
    validate_certs: false
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
            username=dict(type='str', required=True),
            password=dict(type='str', required=True, no_log=True),
            service_name=dict(type='str', required=True),
            mcs_url=dict(type='str', required=True),
            mcs_port=dict(type='str', default='8443', required=False),
            state=dict(type='str', required=True),
            validate_certs=dict(type='bool', default='False'),
        )
    )

    maprUsername = module.params['username']
    maprPassword = module.params['password']
    serviceName = module.params['service_name'].lower()
    serviceState = module.params['state'].lower()
    mcsUrl = module.params['mcs_url']
    mcsPort = module.params['mcs_port']
    mapr_default_service_state = ['start', 'stop', 'restart']

    # Hack to add basic auth username and password the way fetch_url expects
    module.params['url_username'] = maprUsername
    module.params['url_password'] = maprPassword

    def get_current_hostname():
        cmd = module.get_bin_path('hostname', True)
        rc, out, err = module.run_command(cmd)
        if rc != 0:
            module.fail_json(
                msg="Command failed rc=%d, out=%s, err=%s" % (rc, out, err))
        return out.strip()

    if not maprUsername or not maprPassword:
        module.fail_json(msg="Username and Password should be defined")
    elif not serviceName or not serviceState:
        module.fail_json(msg="Service Name & Service State should be defined")
    elif not mcsUrl:
        module.fail_json(msg="MCS Url Should be Defined")
    elif serviceState not in mapr_default_service_state:
        module.fail_json(msg="state should be start/stop/restart only")
    else:
        host = get_current_hostname()
        url_parameters = "?action=" + serviceState + "&nodes=" + \
            str(host) + "&name=" + serviceName
        complete_url = "https://" + mcsUrl + ":" + mcsPort + \
            "/rest/node/services" + url_parameters
        headers = {'Content-Type': 'application/json'}
        (resp, info) = fetch_url(module,
                                 complete_url,
                                 headers=headers,
                                 method='GET')
        if info['status'] >= 400:
            module.fail_json(msg="Unauthorized Access to MapR Services")
        elif info['status'] == 200:
            body = json.loads(resp.read())
            if body['status'] == 'ERROR':
                module.fail_json(msg=body['errors'][0]['desc'])
            else:
                module.exit_json(changed=True)
        else:
            module.fail_json(
                msg="Unknown Response from MapR API: %s" % resp.read())


if __name__ == '__main__':
    main()
