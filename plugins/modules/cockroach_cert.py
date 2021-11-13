#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_cert
short_description: Manage user certificates in a cockroach cluster
description:
    - Manage user certificates in a cockroach cluster
version_added: "0.4.0"
options:
    name:
        description:
            - The name of the user to generate certificate for
        required: true
        default: None

notes:
author: Oscar C, based on the work of Mikael Sandstrom, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
- name: create a certificate for a user
  cockroach_cert:
    name: user1
    path: "/var/lib/cockroach"
"""

from ansible.module_utils.basic import *
import os


# Check if the service exists
def check_user_has_certificate(module, msg, path, name, certs_dir):
    command = "%s/cockroach cert list" % (path)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    # module.exit_json(msg=rc)
    if rc != 0:
        msg[0] = "Something went wrong, stderr: %s" % (stderr)

    if "client." + name.lower() + ".crt" in stdout.lower():
        return True
    else:
        return False


def create_certificate_for_user(module, msg, path, name, certs_dir, ca_key):
    command = "%s/cockroach cert create-client %s" % (path, name)
    if certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    if ca_key:
        command += " --ca-key=%s" % (ca_key)

    # module.fail_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Creating user certificate for %s failed. %s" % (name, stderr)
        return False
    else:
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            name=dict(required=True, aliases=["user_name", "user"]),
            path=dict(required=False),
            certs_dir=dict(required=False),
            ca_key=dict(required=False),
        ),
    )

    name = module.params["name"]
    path = module.params["path"]
    certs_dir = module.params["certs_dir"]
    ca_key = module.params["ca_key"]

    if not path:
        try:
            command = "cockroach version"
            module.run_command(command)
        except OSError as e:
            msg[0] = "Couldnt find cockroach executable. Check the path. stderr: %s" % (
                e
            )
            module.fail_json(msg=msg[0], failed=True)

    if not check_user_has_certificate(module, msg, path, name, certs_dir):
        if create_certificate_for_user(module, msg, path, name, certs_dir, ca_key):
            msg[0] = "Successfully created certificate for user %s " % (name)
            module.exit_json(msg=msg[0], changed=True)
        else:
            module.fail_json(msg=msg[0], changed=False)
    else:
        msg[0] = "User %s already has certificate" % (name)
        module.exit_json(msg=msg[0], changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


if __name__ == "__main__":
    main()
