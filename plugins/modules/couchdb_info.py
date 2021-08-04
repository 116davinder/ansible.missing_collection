#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: couchdb_info
short_description: Get information about Couchdb Cluster.
description:
  - Get information about Couchdb Cluster.
  - U(https://docs.couchdb.org/en/stable/api/index.html)
version_added: 0.1.1
options:
  scheme:
    description:
      - http scheme for couchdb.
    required: false
    type: str
    choices: ['http', 'https']
    default: 'http'
  host:
    description:
      - hostname/ip of couchdb.
    required: false
    type: str
    default: 'localhost'
  port:
    description:
      - port number of couchdb.
    required: false
    type: str
    default: '5984'
  user:
    description:
      - couchdb username.
    required: false
    type: str
    default: 'admin'
  password:
    description:
      - password for couchdb I(user).
    required: false
    type: str
    default: 'password'
  command:
    description:
      - commands to fetch cluster information.
    required: false
    type: str
    choices: ["all_dbs", "active_tasks", "membership", "scheduler/jobs", "scheduler/docs", "up"]
    default: 'all_dbs'
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
  - urllib
"""

EXAMPLES = """
- name: get list of databases
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'all_dbs'

- name: get list of active tasks
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'active_tasks'

- name: get list of nodes in cluster
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'membership'

- name: get list of scheduled jobs
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'scheduler/jobs'

- name: get list of scheduler docs
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'scheduler/docs'

- name: get node status
  community.missing_collection.couchdb_info:
    scheme: 'http'
    host: 'localhost'
    port: '5984'
    user: 'admin'
    password: 'password'
    command: 'up'
"""

RETURN = """
dbs:
  description: list of all databases.
  returned: when command I(all_dbs) is defined and success.
  type: list
  sample: ["_replicator","_users","test"]
active_tasks:
  description: list of active tasks.
  returned: when command I(active_tasks) is defined and success.
  type: list
  sample: [
    {
        "changes_done": 64438,
        "database": "mailbox",
        "pid": "<0.12986.1>",
        "progress": 84,
        "started_on": 1376116576,
        "total_changes": 76215,
        "type": "database_compaction",
        "updated_on": 1376116619
    }
  ]
membership:
  description: list of members in the cluster.
  returned: when command I(membership) is defined and success.
  type: dict
  sample: {
      "all_nodes": [
          "node1@127.0.0.1",
          "node2@127.0.0.1",
          "node3@127.0.0.1"
      ],
      "cluster_nodes": [
          "node1@127.0.0.1",
          "node2@127.0.0.1",
          "node3@127.0.0.1"
      ]
  }
jobs:
  description: list of all scheduler jobs.
  returned: when command I(scheduler/jobs) is defined and success.
  type: dict
  sample: {
      "jobs": [
          {
              "database": "_replicator",
              "doc_id": "cdyno-0000001-0000003",
              "history": [],
              "id": "8f5b1bd0be6f9166ccfd36fc8be8fc22+continuous",
              "info": {},
              "node": "node1@127.0.0.1",
              "pid": "<0.1850.0>",
              "source": "http://myserver.com/foo",
              "start_time": "2017-04-29T05:01:37Z",
              "target": "http://adm:*****@localhost:15984/cdyno-0000003/",
              "user": null
          }
      ],
      "offset": 0,
      "total_rows": 1
  }
docs:
  description: list of all scheduler docs.
  returned: when command I(scheduler/docs) is defined and success.
  type: dict
  sample: {
      "docs": [
          {
              "database": "_replicator",
              "doc_id": "cdyno-0000001-0000002",
              "error_count": 0,
              "id": "e327d79214831ca4c11550b4a453c9ba+continuous",
              "info": {},
              "last_updated": "2017-04-29T05:01:37Z",
              "node": "node2@127.0.0.1",
              "source_proxy": null,
              "target_proxy": null,
              "source": "http://myserver.com/foo",
              "start_time": "2017-04-29T05:01:37Z",
              "state": "running",
              "target": "http://adm:*****@localhost:15984/cdyno-0000002/"
          }
      ],
      "offset": 0,
      "total_rows": 1
  }
up:
  description: status of node.
  returned: when command I(up) is defined and success.
  type: dict
  sample: {"status": "ok", "seeds":{}}
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        scheme=dict(choices=["http", "https"], default="http"),
        host=dict(default="localhost"),
        port=dict(default="5984"),
        user=dict(default="admin"),
        password=dict(default="password", no_log=True),
        command=dict(
            choices=["all_dbs", "active_tasks", "membership", "scheduler/jobs", "scheduler/docs", "up"],
            default="all_dbs"
        ),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    _auth = (
        module.params["user"],
        module.params["password"]
    )

    _url = module.params["scheme"] + "://" + module.params["host"] + ":" \
        + module.params["port"] + "/_" + module.params["command"]

    headers = {"Content-Type": "application/json"}

    r = requests.get(
        _url,
        auth=_auth,
        headers=headers
    )
    if r.status_code == 200:
        if module.params["command"] == "all_dbs":
            module.exit_json(dbs=r.json())
        elif module.params["command"] == "active_tasks":
            module.exit_json(active_tasks=r.json())
        elif module.params["command"] == "membership":
            module.exit_json(membership=r.json())
        elif module.params["command"] == "scheduler/jobs":
            module.exit_json(jobs=r.json())
        elif module.params["command"] == "scheduler/docs":
            module.exit_json(docs=r.json())
        elif module.params["command"] == "up":
            module.exit_json(up=r.json())
        else:
            module.fail_json(msg="unknown parameters")
    else:
        module.fail_json(msg=r.json())


if __name__ == "__main__":
    main()
