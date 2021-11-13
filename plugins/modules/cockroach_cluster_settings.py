#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_cluster_settings
short_description: Manage settings in a Cockroach cluster
description:
    - Manage settings in a Cockroach cluster
version_added: "0.4.0"
options:
    name:
        description:
            - The name of the setting
        required: true
        default: None
    value:
        description:
            - The value of the setting
        required: true
        default: None
author: Mikael Sandström, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
- name: manage a setting
  cockroach_cluster_settings:
    name: 'diagnostics.reporting.enabled'
    value: False
    path: /var/lib/cockroach
    host: "{{ inventory_hostname }}"
    state: present
"""
import os


def get_current_setting(module, msg, path, host, port, name, value, certs_dir):

    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "show cluster setting %s"' % (name)

    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg = "Something went wrong, stderr: %s" % (stderr)

    if value.lower() in stdout.lower():
        return True
    else:
        return False


def enforce_setting(module, msg, path, host, port, name, value, certs_dir):

    currval = get_current_setting(module, msg, path, host, port, name, value, certs_dir)
    if currval:
        module.exit_json(msg="Nothing to change", changed=False)

    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += " --execute \"set cluster setting %s = '%s' \"" % (name, value)

    (rc, stdout, stderr) = module.run_command(command)

    if rc != 0:
        msg = "stderr: %s" % (stderr)
        module.fail_json(msg=msg)
    else:
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True),
            value=dict(required=True),
            host=dict(required=False, default="localhost"),
            port=dict(required=False, default=26257),
            state=dict(default="present", choices=["present", "absent"]),
            path=dict(required=False),
            certs_dir=dict(required=False),
        ),
    )

    name = module.params["name"]
    value = module.params["value"]
    host = module.params["host"]
    port = module.params["port"]
    state = module.params["state"]
    path = module.params["path"]
    certs_dir = module.params["certs_dir"]

    if not path:
        try:
            command = "cockroach version"
            module.run_command(command)
        except OSError as e:
            msg = "Couldnt find cockroach executable. Check the path. stderr: %s" % (e)
            module.fail_json(msg=msg, failed=True)

    if state == "present":
        if enforce_setting(module, msg, path, host, port, name, value, certs_dir):
            msg = "Successfully changed cluster setting: %s to %s" % (name, value)
            module.exit_json(msg=msg, changed=True)
        else:
            module.fail_json(msg=msg, changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
