#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_privs
short_description: Manage user privileges in a cockroach db
description:
    - Manage user privileges in a cockroach db
version_added: 0.4.0
options:
  name:
    description:
      - the name of the user to set permissions
    required: true
    default: None
  db:
    description:
      - Name of the database to set permissions in
    required: true
    default: None
  privs:
    description:
      - Privileges for the user
    required: true
    default: None
author:
    - Oscar C
    - Mikael Sandstrom @oravirt
"""

EXAMPLES = """
# Grant ALL privileges to user1 on db1
cockroach_privs: name=user1 db=db1 privs=ALL path=/var/lib/cockroach
"""
from ansible.module_utils.basic import AnsibleModule
import os

# Check if the service exists
def check_user_privs(module, msg, path, host, port, name, certs_dir, db, privs):
    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "SHOW GRANTS ON DATABASE %s FOR %s;"' % (db, name)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    # module.exit_json(msg=rc)
    if rc != 0:
        msg[0] = "Something went wrong, stderr: %s" % (stderr)

    if privs.lower() in stdout.lower():
        return True
    else:
        return False


def set_user_privs(module, msg, path, host, port, name, certs_dir, db, privs):
    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "GRANT %s ON DATABASE %s TO %s;"' % (privs, db, name)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Setting user privileges for db %s failed. %s" % (db, stderr)
        return False
    else:
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=["username", "user"]),
            host=dict(required=False, default="localhost"),
            port=dict(required=False, default=26257),
            path=dict(required=False),
            certs_dir=dict(required=False),
            db=dict(required=True),
            privs=dict(required=False, default="ALL"),
        ),
    )

    name = module.params["name"]
    host = module.params["host"]
    port = module.params["port"]
    path = module.params["path"]
    certs_dir = module.params["certs_dir"]
    db = module.params["db"]
    privs = module.params["privs"]

    if not path:
        try:
            command = "cockroach version"
            module.run_command(command)
        except OSError as e:
            msg[0] = "Couldnt find cockroach executable. Check the path. stderr: %s" % (
                e
            )
            module.fail_json(msg=msg[0], failed=True)

    if not check_user_privs(module, msg, path, host, port, name, certs_dir, db, privs):
        if set_user_privs(module, msg, path, host, port, name, certs_dir, db, privs):
            msg[0] = "Successfully set permissions for user %s on db %s " % (name, db)
            module.exit_json(msg=msg[0], changed=True)
        else:
            module.fail_json(msg=msg[0], changed=False)
    else:
        msg[0] = "User %s permissions already set on %s " % (name, db)
        module.exit_json(msg=msg[0], changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


if __name__ == "__main__":
    main()
