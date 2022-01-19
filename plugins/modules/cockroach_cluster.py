#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_cluster
short_description: Manage a cockroach cluster
description:
    - Manage a cockroach cluster
version_added: "0.4.0"
options:
    name:
        description:
            - The name of the service
        required: true
        default: None
author: Mikael Sandström, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
- name: create a master node
  cockroach_cluster:
    path: "/var/lib/cockroach"
    host: "{{ inventory_hostname }}"
    state: started

- name: join a node to a cluster
  cockroach_cluster:
    path: "/var/lib/cockroach"
    host: "{{ inventory_hostname }}"
    join: true
    cluster_master: "node1:{{ port }}"
    state: started
"""

from ansible.module_utils.basic import *
import os

# Check if the service exists
def check_node_started(module, msg, path):

    command = "ps -ef"
    (rc, stdout, stderr) = module.run_command(command)
    searchstring = "%s/cockroach" % (path)
    if rc != 0:
        msg[0] = "Something went wrong, stderr: %s" % (stderr)

    if searchstring in stdout.lower():
        return True
    else:
        return False


def start_node(
    module,
    msg,
    path,
    store,
    host,
    port,
    http_port,
    join,
    cache,
    log_dir,
    certs_dir,
    locality,
    cluster_master,
):

    command = "nohup %s/cockroach start --http-port=%s --port=%s --host=%s " % (
        path,
        http_port,
        port,
        host,
    )
    if store:
        command += " --store=%s" % (store)
    if join:
        command += " --join=%s:%s" % (cluster_master, port)
    if cache:
        command += " --cache=%s" % (cache)
    if locality:
        command += " --locality=%s" % (locality)
    if log_dir:
        command += " --log-dir %s" % (log_dir)
    if not certs_dir:
        command += " --insecure "
    elif certs_dir:
        command += " --certs-dir %s" % (certs_dir)
    command += " --background"

    # module.exit_json(msg=command)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Starting failed. %s" % (stderr)
        return False
    else:
        msg[0] = "Successfully started node - %s " % (stdout)
        return True


def stop_node(module, msg, path, host, port, certs_dir):

    command = "%s/cockroach quit --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Failed to stop node. %s" % (stderr)
        return False
    else:
        msg[0] = "Successfully stopped node - %s" % (stdout.strip())
        return True


def status_node(module, msg, path):

    command = "%s/cockroach node status" % (path)
    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg[0] = "Failed to check status for node: %s" % (stderr)
        return False
    else:
        msg[0] = stdout
        return True


def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            store=dict(required=False),
            state=dict(default="started", choices=["started", "stopped", "status"]),
            path=dict(required=False),
            cache=dict(required=False),
            log_dir=dict(required=False),
            certs_dir=dict(required=False),
            locality=dict(required=False),
            port=dict(default=26257),
            http_port=dict(default=8080),
            host=dict(default="localhost"),
            join=dict(required=False, type=bool),
            cluster_master=dict(required=False),
        ),
    )

    store = module.params["store"]
    state = module.params["state"]
    path = module.params["path"]
    cache = module.params["cache"]
    log_dir = module.params["log_dir"]
    certs_dir = module.params["certs_dir"]
    locality = module.params["locality"]
    port = module.params["port"]
    http_port = module.params["http_port"]
    host = module.params["host"]
    join = module.params["join"]
    cluster_master = module.params["cluster_master"]

    if not path:
        try:
            command = "cockroach version"
            module.run_command(command)
        except OSError as e:
            msg[0] = "Couldnt find cockroach executable. Check the path. stderr: %s" % (
                e
            )
            module.fail_json(msg=msg[0], failed=True)

    if not store:
        store = "%s/cockroach-data" % (path)

    if state == "started":
        if not check_node_started(module, msg, path):
            if start_node(
                module,
                msg,
                path,
                store,
                host,
                port,
                http_port,
                join,
                cache,
                log_dir,
                certs_dir,
                locality,
                cluster_master,
            ):
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "Already running"
            module.exit_json(msg=msg[0], changed=False)

    elif state == "stopped":
        if check_node_started(module, msg, path):
            if stop_node(module, msg, path, host, port, certs_dir):
                # msg[0] = 'Successfully dropped database %s ' % (name)
                module.exit_json(msg=msg[0], changed=True)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "Node already stopped"
            module.exit_json(msg=msg[0], changed=False)

    elif state == "status":
        if check_node_started(module, msg, path):
            if status_node(module, msg, path, port, host, certs_dir):
                # msg[0] = 'Successfully dropped database %s ' % (name)
                module.exit_json(msg=msg[0], changed=False)
            else:
                module.fail_json(msg=msg[0], changed=False)
        else:
            msg[0] = "Node not running"
            module.exit_json(msg=msg[0], changed=False)

    module.exit_json(msg="Unhandled exit", changed=False)


if __name__ == "__main__":
    main()
