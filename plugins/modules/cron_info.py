#!/usr/bin/python3
# -*- coding: utf-8 -*-

# Copyright 2021 Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = '''
---
module: cron_info
short_description: Get Information from Crontab.
description:
  - Get Information from Crontab.
  - U(https://pypi.org/project/python-crontab/)
version_added: 0.4.0
options:
  user:
    description:
      - crontab user.
      - mutually exclusive to I(tabfile).
    required: false
    type: str
    default: 'dpal'
  tabfile:
    description:
      - crontab file location on system.
      - mutually exclusive to I(user).
    required: false
    type: str
  use_regex:
    description:
      - filter crons based on python regex.
      - can be used when I(get_crons_by_command) and I(get_crons_by_comment).
    required: false
    type: str
  match_string:
    description:
      - it can be a string.
      - it can be regex when I(use_regex).
    required: false
    type: str
  schedule:
    description:
      - cron schedule pattern and used when I(validate_cron_time).
      - example B(4 16 * * *)
    required: false
    type: str
  list_all_crons:
    description:
      - get list of all crons for given I(user)/I(tabfile).
    required: false
    type: bool
  get_crons_by_command:
    description:
      - get list of cron which matches to I(match_string) command and given I(user)/I(tabfile).
    required: false
    type: bool
  get_crons_by_comment:
    description:
      - get list of cron which matches to I(match_string) comment and given I(user)/I(tabfile).
    required: false
    type: bool
  get_crons_by_time:
    description:
      - get list of cron which matches to I(match_string) time and given I(user)/I(tabfile).
    required: false
    type: bool
  validate_cron_time:
    description:
      - validate cron schedule or time format?
    required: false
    type: bool
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - python-crontab
  - re
'''

EXAMPLES = '''
- name: get all crons for dpal user
  community.missing_collection.cron_info:
    list_all_crons: true
    user: 'dpal'

- name: get all crons by command for dpal user (python command)
  community.missing_collection.cron_info:
    get_crons_by_command: true
    user: 'dpal'
    match_string: '.py'

- name: get all crons by comment for dpal user
  community.missing_collection.cron_info:
    get_crons_by_comment: true
    user: 'dpal'
    match_string: 'python'

- name: get all crons by time for dpal user
  community.missing_collection.cron_info:
    get_crons_by_time: true
    user: 'dpal'
    match_string: '4 16 * * *'

- name: check if given crontime is valid or not
  community.missing_collection.cron_info:
    validate_cron_time: true
    schedule: '2 14 * * *'
'''

RETURN = """
cron:
  description: list of the cron jobs
  returned: when success and not I(validate_cron_time).
  type: list
  sample: [
    {
      "command": "ls -alh > /dev/null",
      "comment": "check dirs",
      "enabled": true,
      "marker": "Ansible",
      "slices": "0 2,5 * * *",
      "special": false,
      "user": "None",
      "valid": true
    }
  ]
valid:
  description: validate given cron schedule/time.
  returned: when I(validate_cron_time) and success.
  type: bool
  sample: true
"""

from ansible.module_utils.basic import AnsibleModule
from crontab import CronTab, CronSlices
import re


def cron_items_to_list(items):
    crons = []
    for cron in items:
        if str(cron) != "":
            crons.append({
                "user": str(cron.user),
                "valid": cron.valid,
                "enabled": cron.enabled,
                "special": cron.special,
                "comment": str(cron.comment),
                "command": str(cron.command),
                "slices": str(cron.slices),
                "marker": str(cron.marker),
            })
    return crons


def main():
    module = AnsibleModule(
        argument_spec=dict(
            # default value for user to bypass required_one_of check
            # incase of validate_cron_time
            user=dict(default="dpal"),
            tabfile=dict(),
            use_regex=dict(default=False),
            match_string=dict(),
            schedule=dict(),
            list_all_crons=dict(type=bool),
            get_crons_by_command=dict(type=bool),
            get_crons_by_comment=dict(type=bool),
            get_crons_by_time=dict(type=bool),
            validate_cron_time=dict(type=bool),
        ),
        required_one_of=(
            ("user", "tabfile"),
        ),
        required_if=(
            ("get_crons_by_command", True, ["match_string", "use_regex"]),
            ("get_crons_by_comment", True, ["match_string", "use_regex"]),
            ("get_crons_by_time", True, ["match_string", "use_regex"]),
            ("validate_cron_time", True, ["schedule"]),
        )
    )

    cron = CronTab(user=module.params["user"], tabfile=module.params["tabfile"])

    if module.params['list_all_crons']:
        crons = cron.lines
    elif module.params['get_crons_by_command']:
        if module.params["use_regex"]:
            crons = cron.find_command(
                re.compile(r"{}".format(module.params["match_string"]))
            )
        else:
            crons = cron.find_command(module.params["match_string"])
    elif module.params['get_crons_by_comment']:
        if module.params["use_regex"]:
            crons = cron.find_comment(
                re.compile(r"{}".format(module.params["match_string"]))
            )
        else:
            crons = cron.find_comment(module.params["match_string"])
    elif module.params['get_crons_by_time']:
        crons = cron.find_time(module.params["match_string"])

    elif module.params['validate_cron_time']:
        module.exit_json(valid=CronSlices.is_valid(module.params["schedule"]))
    else:
        module.fail_json(msg="unknown parameters")

    module.exit_json(crons=cron_items_to_list(crons))


if __name__ == '__main__':
    main()
