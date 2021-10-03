#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2018 Davinder Pal <dpsangwal@gmail.com>
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: mapr_blacklistuser
version_added: 0.4.0
author: "Davinder Pal (@116davinder)"
short_description: Add user to mapr blacklist
description:
   - Manage MapR BlackList Services
     if you want to remove user from blacklist
     (https://mapr.com/docs/52/SecurityGuide/HowTicketsWork.html)
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
  validate_certs:
    description:
      - If C(no), SSL certificates will not be validated.
        This should only be used for personal self-signed certificates.
    required: false
    default: 'yes'
    type: bool
  list_user:
    description:
      - If C(no), SSL certificates will not be validated.
        This should only be used for personal self-signed certificates.
    required: false
    type: bool
  user:
    description:
      - If C(no), SSL certificates will not be validated.
        This should only be used for personal self-signed certificates.
    required: false
    type: string

    version_added: 2.6.x

'''

EXAMPLES = '''
- mapr_blacklistuser:
    username: mapr
    password: mapr
    mcs_url: demo.mapr.com
    mcs_port: 8443
    validate_certs: false
    list_user: true

- mapr_blacklistuser:
    username: mapr
    password: mapr
    mcs_url: demo.mapr.com
    mcs_port: 8443
    validate_certs: false
    user: test
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
            mcs_url=dict(type='str', required=True),
            mcs_port=dict(type='str', default='8443', required=False),
            validate_certs=dict(type='bool', default=False),
            list_user=dict(type='bool', default=True, required=False),
            user=dict(type='str', required=False),
        )
    )

    maprUsername = module.params['username']
    maprPassword = module.params['password']
    mcsUrl = module.params['mcs_url']
    mcsPort = module.params['mcs_port']

    # Hack to add basic auth username and password the way fetch_url expects
    module.params['url_username'] = maprUsername
    module.params['url_password'] = maprPassword

    if not maprUsername or not maprPassword:
        module.fail_json(msg="Username and Password should be defined")
    elif not mcsUrl:
        module.fail_json(msg="MCS Url Should be Defined")
    elif module.params['list_user'] and module.params['user'] is not None:
        module.fail_json(msg="Only define one of list_user or user")
    else:
        if module.params['list_user']:
            url_parameters = "listusers"
        elif module.params['user'] is not None:
            url_parameters = "users?name=" + module.params['user']
        complete_url = "https://" + mcsUrl + ":" + mcsPort + \
            "/rest/blacklist/" + url_parameters
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
