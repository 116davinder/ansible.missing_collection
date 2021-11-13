#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_user
short_description: Manage users in a cockroach cluster
description:
    - Manage users in a cockroach cluster
version_added: 0.4.0
options:
    name:
        description:
            - The name of the user
        required: true
        default: None

notes:
author:
    - Oscar C
    - Mikael Sandström, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
# Create a user
cockroach_user: name=user1 path=/var/lib/cockroach host={{ inventory_hostname }} state=present

# Delete a user
cockroach_user: name=user1 path=/var/lib/cockroach host={{ inventory_hostname }} state=absent

"""

from ansible.module_utils.basic import *
import os

# Check if the service exists
def check_user_exists(module, msg, path, host, port, name, certs_dir):
    command = "%s/cockroach user ls --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    # module.exit_json(msg=rc)
    if rc != 0:
        msg[0] = "Something went wrong, stderr: %s" % (stderr)

    if name.lower() in stdout.lower():
        return True
    else:
        return False


def create_user(module, msg, path, host, port, name, certs_dir):
    command = "%s/cockroach user set %s  --host=%s --port=%s " % (
        path,
        name,
        host,
        port,
    )
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Creating user %s failed. %s. Command: %s" % (name, stderr, command)
        return False
    else:
        return True


def remove_user(module, msg, path, host, port, name, certs_dir):

    command = "%s/cockroach user rm %s --host=%s --port=%s " % (path, name, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    # command += ' user rm %s' % (name)

    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Removing user %s failed: %s" % (name, stderr)
        return False
    else:
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=["user_name", "user"]),
            host=dict(required=False, default="localhost"),
            port=dict(required=False, default=26257),
            state=dict(default="present", choices=["present", "absent"]),
            path=dict(required=False),
            certs_dir=dict(required=False),
        ),
    )

    name = module.params["name"]
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
            msg[0] = "Couldnt find cockroach executable. Check the path. stderr: %s" % (
                e
            )
            module.fail_json(msg=msg[0], failed=True)

    if state == "present":
        if not check_user_exists(module, msg, path, host, port, name, certs_dir):
            if create_user(module, msg, path, host, port, name, certs_dir):
                msg[0] = "Successfully created user %s " % (name)
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "User %s already exists" % (name)
            module.exit_json(msg=msg[0], changed=False)

    elif state == "absent":
        if check_user_exists(module, msg, path, host, port, name, certs_dir):
            if remove_user(module, msg, path, host, port, name, certs_dir):
                msg[0] = "Successfully deleted user %s " % (name)
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "User %s doesn't exist" % (name)
            module.exit_json(msg=msg[0], changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


if __name__ == "__main__":
    main()
