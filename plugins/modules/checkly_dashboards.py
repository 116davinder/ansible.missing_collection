#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: checkly_dashboards
short_description: Management of the checkly Dashboards.
description:
  - Management of the checkly Dashboards.
  - U(https://www.checklyhq.com/docs/api#tag/Dashboards)
version_added: 0.3.0
options:
  url:
    description:
      - checkly api.
    required: false
    type: str
    default: 'https://api.checklyhq.com/v1/dashboards/'
  api_key:
    description:
      - api key for checkly.
    required: true
    type: str
  command:
    description:
      - type of operation on dashboards.
    required: false
    type: str
    choices: ["create", "update", "delete"]
    default: "create"
  id:
    description:
      - id of dashboard.
      - required only for I(delete) and I(update).
    required: false
    type: str
  custom_domain:
    description:
      - A custom user domain, e.g. "status.example.com".
      - See the docs on updating your DNS and SSL usage.
    required: false
    type: str
  custom_url:
    description:
      - A subdomain name under "checklyhq.com".
      - Needs to be unique across all users.
    required: false
    type: str
  header:
    description:
      - A piece of text displayed at the top of your dashboard.
    required: false
    type: str
    default: "Managed by Ansible Automation"
  hide_tags:
    description:
      - Show or hide the tags on the dashboard.
    required: false
    type: bool
    default: false
  logo:
    description:
      - A URL pointing to an image file.
      - example I(https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png)
    required: false
    type: str
  paginate:
    description:
      - Determines of pagination is on or off.
    required: false
    type: bool
    default: true
  pagination_rate:
    description:
      - How often to trigger pagination in seconds.
    required: false
    type: int
    choices: [30, 60, 300]
    default: 60
  refresh_rate:
    description:
      - How often to refresh the dashboard in seconds.
    required: false
    type: int
    choices: [60, 300, 600]
    default: 60
  tags:
    description:
      - A list of one or more tags that filter which checks to display on the dashboard.
    required: false
    type: list
    default: []
  width:
    description:
      - Determines whether to use the full screen or focus in the center.
    required: false
    type: str
    choices: ["FULL", "960PX"]
    default: "FULL"
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
- name: create a dashboard
  community.missing_collection.checkly_dashboards:
    api_key: '4a7734debb54464e9fefe8b4f14b896e'
    command: 'create'
    custom_domain: '6605c28f.axway.com'
    custom_url: "6605c28f"
    header: 'Managed by Ansible Automation'
    tags:
      - 'api'
      - 'axway'
    logo: 'https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png'
  register: __

- name: update a dashboard
  community.missing_collection.checkly_dashboards:
    api_key: '4a7734debb54464e9fefe8b4f14b896e'
    command: 'update'
    custom_domain: '6605c28f.axway.com'
    custom_url: "6605c28f"
    header: 'Managed by Ansible Automation'
    tags:
      - 'api'
      - 'axway'
    id: '{{ __.result.dashboardId }}'
    logo: 'https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png'

- name: delete a dashboard
  community.missing_collection.checkly_dashboards:
    api_key: '4a7734debb54464e9fefe8b4f14b896e'
    command: 'delete'
    id: '{{ __.result.dashboardId }}'
"""

RETURN = """
result:
  description: result of checkly api.
  returned: when command is I(create)/I(update) and success.
  type: dict
  sample: {
    "customUrl": "string",
    "customDomain": "string",
    "logo": "string",
    "header": "string",
    "width": "FULL",
    "refreshRate": 60,
    "paginate": true,
    "paginationRate": 30,
    "tags": [],
    "hideTags": false,
    "dashboardId": "string"
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        url=dict(default="https://api.checklyhq.com/v1/dashboards/"),
        api_key=dict(required=True, no_log=True),
        command=dict(choices=["create", "update", "delete"], default="create"),
        id=dict(),
        custom_domain=dict(),
        custom_url=dict(),
        header=dict(default="Managed by Ansible Automation"),
        hide_tags=dict(type=bool, default=False),
        logo=dict(),
        paginate=dict(type=bool, default=True),
        pagination_rate=dict(type=int, choices=[30, 60, 300], default=60),
        refresh_rate=dict(type=int, choices=[60, 300, 600], default=60),
        tags=dict(type=list, default=[]),
        width=dict(choices=["FULL", "960PX"], default="FULL"),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )
    headers = {
        "Authorization": "Bearer {}".format(module.params["api_key"]),
        "Content-Type": "application/json"
    }
    data = {
        "header": module.params["header"],
        "hideTags": module.params["hide_tags"],
        "paginate": module.params["paginate"],
        "paginationRate": module.params["pagination_rate"],
        "refreshRate": module.params["refresh_rate"],
        "tags": module.params["tags"],
        "width": module.params["width"]
    }
    if module.params["custom_domain"]:
        data["customDomain"] = module.params["custom_domain"]
    if module.params["custom_url"]:
        data["customUrl"] = module.params["custom_url"]
    if module.params["logo"]:
        data["logo"] = module.params["logo"]

    if module.params["command"] == "create":
        r = requests.post(module.params["url"], json=data, headers=headers)
    # update doesn't work getting conflict error message.
    elif module.params["command"] == "update":
        r = requests.put(
            module.params["url"] + module.params["id"],
            json=data,
            headers=headers
        )
    else:
        r = requests.delete(
            module.params["url"] + module.params["id"],
            headers=headers
        )
    if r.status_code in [200, 201] and module.params["command"] in ["create", "update"]:
        module.exit_json(changed=True, result=r.json())
    elif r.status_code == 204 and module.params["command"] == "delete":
        module.exit_json(changed=True)
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
