#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function

__metaclass__ = type


DOCUMENTATION = """
module: appd_event
short_description: create application deployment events for appdynamics.
description:
  - create application deployment events for appdynamics.
  - U(https://docs.appdynamics.com/21.10/en/extend-appdynamics/appdynamics-apis/alert-and-respond-api/events-and-action-suppression-api#EventsandActionSuppressionAPI-CreateEvents)
version_added: 0.4.0
options:
  scheme:
    description:
      - scheme for appdynamics controller.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'https'
  host:
    description:
      - hostname/ip of appdynamics controller.
      - example I(demo.appdynamics.com)
    required: true
    type: str
  port:
    description:
      - port number of appdynamics controller.
    required: false
    type: str
    default: '443'
  user:
    description:
      - username of appdynamics controller.
    required: true
    type: str
  password:
    description:
      - password of appdynamics controller.
    required: true
    type: str
  id:
    description:
      - provide either application name or application id.
    required: true
    type: str
    aliases: ['application_id', 'application_name']
  summary:
    description:
      - provide a summary describing the event.
    required: true
    type: str
  comment:
    description:
      - provide a comment describing the event.
    required: false
    type: str
    default: ''
  eventtype:
    description:
      - type of appdynamics event.
      - Only supported option B(APPLICATION_DEPLOYMENT).
    required: false
    type: str
    default: 'APPLICATION_DEPLOYMENT'
  severity:
    description:
      - provide a severity level for the event.
    required: false
    type: str
    choices: ['INFO', 'WARN', 'ERROR']
    default: 'INFO'
  output:
    description:
      - provide a output in I(JSON) format if any.
    required: false
    type: str
    default: 'JSON'
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create application deployment event to AppDynamics
  community.missing_collection.appd_event:
    scheme: 'https'
    host: 'demo.appdynamics.com'
    port: '443'
    user: 'testUser'
    password: 'testPassword'
    id: 'test_application'
    summary: 'new release of application 0.0.1'
    eventtype: 'APPLICATION_DEPLOYMENT'
    severity: 'INFO'
    comment: 'deployed by ansible automation'
"""

RETURN = """
"""

from ansible.module_utils.basic import AnsibleModule
import requests
from requests.auth import HTTPBasicAuth


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="https"),
        host=dict(required=True),
        port=dict(default="443"),
        user=dict(required=True),
        password=dict(required=True, no_log=True),
        id=dict(required=True, aliases=["application_id", "application_name"]),
        summary=dict(required=True),
        comment=dict(default=""),
        eventtype=dict(default="APPLICATION_DEPLOYMENT"),
        severity=dict(choices=["INFO", "WARN", "ERROR"], default="INFO"),
        output=dict(default="JSON"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    module.warn("untested module, please report the issue")
    # http://demo.appdynamics.com/controller/rest/applications/5/events
    # http://<controller_host>:<controller_port>/controller/rest/
    # /controller/rest/applications/application_id/events
    _url = (
        module.params["scheme"]
        + "://"
        + module.params["host"]
        + ":"
        + module.params["port"]
        + "/controller/rest/applications/"
        + module.params["id"]
        + "/events"
    )

    auth = HTTPBasicAuth(
        username=module.params["user"], password=module.params["password"]
    )
    params = {
        "summary": module.params["summary"],
        "comment": module.params["comment"],
        "eventtype": module.params["eventtype"],
        "severity": module.params["severity"],
        "output": module.params["output"],
    }
    r = requests.post(url=_url, auth=auth, params=params)
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
