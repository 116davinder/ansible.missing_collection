#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: docker_hub_auditlogs_info
short_description: The Audit Logs API endpoints allow you to query audit log events across a namespace.
description:
  - The Audit Logs API endpoints allow you to query audit log events across a namespace.
  - B(Docker audit logs feature is a Pro or Team feature)
  - U(https://docs.docker.com/docker-hub/api/latest/#tag/audit-logs)
version_added: 0.4.0
options:
  url:
    description:
      - docker hub api.
    required: false
    type: str
    default: 'https://hub.docker.com/v2/auditlogs/'
  token:
    description:
      - jwt/Bearer token for docker hub api.
    required: true
    type: str
  account:
    description:
      - Namespace to query audit logs for.
    required: true
    type: str
  action:
    description:
      - action name one of ["repo.tag.push", ...].
      - Optional parameter to filter specific audit log actions.
    required: false
    type: str
  name:
    description:
      - Optional parameter to filter audit log events to a specific name.
      - For repository events, this is the name of the repository.
      - For organization events, this is the name of the organization.
      - For team member events, this is the username of the team member.
    required: false
    type: str
  actor:
    description:
      - Optional parameter to filter audit log events to the specific user who triggered the event.
    required: false
    type: str
  from_date:
    description:
      - Start of the time window you wish to query audit events for.
      - example I(2021-09-01T00:00:00Z)
    required: false
    type: str
  to_date:
    description:
      - End of the time window you wish to query audit events for.
      - example I(2021-09-01T00:00:00Z)
    required: false
    type: str
  page_size:
    description:
      - number of records retrieved in one call.
    required: false
    type: int
    default: 25
  page:
    description:
      - page number of record retrieve call.
    required: false
    type: int
    default: 1
  list_log_events:
    description:
      - Get audit log events for a given namespace.
    required: false
    type: bool
  list_log_actions:
    description:
      - Get audit log actions for a namespace to be used as a filter for querying audit events.
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: get jwt token from docker hub
  community.missing_collection.docker_hub_token:
    username: 'testUser'
    password: 'aDL0xxxxxxxxxxoQt6'
  register: '__'

- name: get all log events which are repo.tag.push
  community.missing_collection.docker_hub_auditlogs_info:
    token: '{{ __.token }}'
    list_log_events: true
    account: 'yourAccount'
    action: 'repo.tag.push'
    from_date: '2021-09-01T00:00:00Z'
    to_date: '2021-10-02T00:00:00Z'

- name: get all log actions
  community.missing_collection.docker_hub_auditlogs_info:
    token: '{{ __.token }}'
    list_log_actions: true
    account: 'yourAccount'
"""

RETURN = """
result:
  description: result of docker hub api.
  returned: when success.
  type: dict
  sample: {
    "logs": [
      {
        "account": "docker",
        "action": "repo.tag.push",
        "name": "docker/example",
        "actor": "docker",
        "data": {
          "digest": "sha256:c1ae9c435032a276f80220c7d9b40f76266bbe79243d34f9cda30b76fe114dfa",
          "tag": "latest"
        },
        "timestamp": "2021-02-19T01:34:35Z",
        "action_description": "pushed the tag latest with the digest sha256:c1ae9c435032a to the repository docker/example"
      }
    ]
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://hub.docker.com/v2/auditlogs/"),
        token=dict(required=True, no_log=True),
        account=dict(required=True),
        action=dict(),
        name=dict(),
        actor=dict(),
        from_date=dict(),
        to_date=dict(),
        page_size=dict(type=int, default=25),
        page=dict(type=int, default=1),
        list_log_events=dict(type=bool),
        list_log_actions=dict(type=bool),
    )

    module = AnsibleModule(
        argument_spec=argument_spec
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["token"]),
        "Content-Type": "application/json"
    }
    params = {
        "page_size": module.params["page_size"],
        "page": module.params["page"]
    }
    if module.params["action"]:
        params["action"] = module.params["action"]
    if module.params["name"]:
        params["name"] = module.params["name"]
    if module.params["actor"]:
        params["actor"] = module.params["actor"]
    if module.params["from_date"]:
        params["from"] = module.params["from_date"]
    if module.params["to_date"]:
        params["to"] = module.params["to_date"]

    if module.params["list_log_events"]:
        url_suffix = module.params["account"]
    elif module.params["list_log_actions"]:
        url_suffix = "{}/actions".format(module.params["account"])
    else:
        module.fail_json("unknown parameters")

    r = requests.get(
        module.params["url"] + url_suffix,
        params=params,
        headers=headers
    )
    if r.status_code == 200:
        module.exit_json(result=r.json())
    else:
        module.fail_json(msg=r.text, code=r.status_code)


if __name__ == "__main__":
    main()
