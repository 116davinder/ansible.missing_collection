#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_db
short_description: Manage databases in a cockroach cluster
description:
    - Manage databases in a cockroach cluster
version_added: 0.4.0
options:
    name:
        description:
            - The name of the database
        required: true
        default: None

notes:
author: Mikael Sandstrom, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
# Create a database
cockroach_db: name=db1 path=/var/lib/cockroach host={{ inventory_hostname }} state=present

# Drop a database
cockroach_db: name=db1 path=/var/lib/cockroach host={{ inventory_hostname }} state=absent

"""
import os


# Check if the service exists
def check_database_exists(module, msg, path, host, port, name, certs_dir):

    # command = "%s/cockroach sql --host=%s --port=%s --insecure --execute \"show databases\"" % (path, host, port)
    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += (
        " --execute \"SELECT datname FROM pg_catalog.pg_database where lower(datname) = lower('%s') \""  # nosec
        % (name)
    )

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    # module.exit_json(msg=rc)
    if rc != 0:
        msg[0] = "Something went wrong, stderr: %s" % (stderr)

    if name.lower() in stdout.lower():
        return True
    else:
        return False


def create_database(module, msg, path, host, port, name, certs_dir):
    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "create database %s"' % (name)

    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Creating database %s failed. %s, command: %s" % (
            name,
            stderr,
            command,
        )
        return False
    else:
        return True


def remove_database(module, msg, path, host, port, name, certs_dir):

    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "drop database %s"' % (name)

    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Removing database %s failed: %s" % (name, stderr)
        return False
    else:
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=["database_name", "db"]),
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
        if not check_database_exists(module, msg, path, host, port, name, certs_dir):
            if create_database(module, msg, path, host, port, name, certs_dir):
                msg[0] = "Successfully created database %s " % (name)
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "Database %s already exists" % (name)
            module.exit_json(msg=msg[0], changed=False)

    elif state == "absent":
        if check_database_exists(module, msg, path, host, port, name, certs_dir):
            if remove_database(module, msg, path, host, port, name, certs_dir):
                msg[0] = "Successfully dropped database %s " % (name)
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "Database %s doesn't exist" % (name)
            module.exit_json(msg=msg[0], changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
