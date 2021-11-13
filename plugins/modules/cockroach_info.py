#!/usr/bin/python
# -*- coding: utf-8 -*-

DOCUMENTATION = """
---
module: cockroach_facts
short_description: Returns facts about a Cockroach Cluster
description:
    - Returns facts about a Cockroach Cluster
version_added: 0.4.0
options:
    host:
        description:
            - The cluster host
        required: false
        default: localhost
    port:
        description:
            - The cluster port
        required: false
        default: 26257
    user:
        description:
            - The cluster user to connect as
        required: True
        default: root
    certs_dir:
        description:
            - Path to certificates on the cluster host

notes:
    - psycopg2 needs to be installed
requirements: [ "psycopg2" ]
author: Mikael Sandström, oravirt@gmail.com, @oravirt
"""

EXAMPLES = """
- name: Gather Facts about CRDB Cluster
  hosts: clusterhosts
  become: true
  vars:
     cockroach_user: cockroach
     path: /var/lib/cockroach/2.1.6
     certs_dir: /var/lib/cockroach/certs
     user: root
  tasks:
    - name: facts
      cockroach_facts:
            user={{ user |default(omit)}}
            path={{ path |default(omit)}}
            host={{ ansible_fqdn }}
            certs_dir={{ certs_dir |default (omit)}}
      tags: facts
      become_user: "{{ cockroach_user }}"
      register: facts

    - debug: msg="version - {{facts.ansible_facts.cockroach_version}}, node_id - {{facts.ansible_facts.node_id}}"
    - debug: msg="org - {{ facts.ansible_facts.cluster_settings['cluster.organization'] }}{% if facts.ansible_facts.enterprise_license is defined %}, license - {{ facts.ansible_facts.enterprise_license }}{% endif %}"

"""
from datetime import datetime

try:
    from OpenSSL import crypto as c
except ImportError:
    pyopenssl_exists = False
else:
    pyopenssl_exists = True

try:
    import psycopg2
except ImportError:
    psycopg2_exists = False
else:
    psycopg2_exists = True


def exec_sql_get(module, cur, query):

    try:
        cur.execute(query)
        result = cur.fetchall()
    except psycopg2.DatabaseError as e:
        msg = e
        module.fail_json(msg=msg, failed=True)

    return result


def get_enterprise_license(module, path, host, port, certs_dir):

    command = "%s/cockroach sql --host=%s --port=%s " % (path, host, port)
    if not certs_dir:
        command += " --insecure"
    elif certs_dir:
        command += " --certs-dir=%s" % (certs_dir)
    command += ' --execute "show cluster setting enterprise.license"'

    (rc, stdout, stderr) = module.run_command(command)
    if rc != 0:
        msg = "Something went wrong, stderr: %s, command: %s" % (stderr, command)
        module.fail_json(msg)
    return stdout


def get_cert_expiry_date(cert):
    datefmt = "%Y%m%d%H%M%SZ"
    cert = c.load_certificate(c.FILETYPE_PEM, file(cert).read())
    return datetime.datetime.strptime(cert.get_notAfter(), datefmt)


# Ansible code
def main():

    msg = [""]

    module = AnsibleModule(
        argument_spec=dict(
            host=dict(required=False, default="localhost"),
            port=dict(required=False, default=26257),
            path=dict(required=False),
            user=dict(required=False, default="root"),
            certs_dir=dict(required=False),
        ),
    )

    host = module.params["host"]
    port = module.params["port"]
    path = module.params["path"]
    user = module.params["user"]
    certs_dir = module.params["certs_dir"]

    cacert = "%s/ca.crt" % (certs_dir)
    nodecert = "%s/node.crt" % (certs_dir)
    clientkey = "%s/client.%s.key" % (certs_dir, user)
    clientcert = "%s/client.%s.crt" % (certs_dir, user)

    if not psycopg2_exists:
        msg = "psycopg2 does not seem to exist. Please install (e.g pip install psycopg2-binary)"
        module.fail_json(msg=msg)

    try:

        # dsn = psycopg2.make_dsn(host=host, port=port, database=database, user=user,
        #                        sslmode='require', sslkey=sslkey,sslcert=sslcert)
        # conn = psycopg2.connect(dsn)
        if certs_dir:
            conn = psycopg2.connect(
                user=user,
                sslmode="require",
                # sslrootcert=rootcert,
                sslkey=clientkey,
                sslcert=clientcert,
                port=port,
                host=host,
            )
        else:
            conn = psycopg2.connect(user=user, sslmode="disable", port=port, host=host)
    except psycopg2.DatabaseError as exc:
        error = exc
        msg = "Could not connect: %s" % (error)
        module.fail_json(msg=msg)

    cur = conn.cursor()

    version_sql = (
        "select value from system.crdb_internal.node_build_info where field = 'Version'"
    )
    node_id_sql = "select distinct(node_id) from system.crdb_internal.node_build_info"
    database_sql = "select datname from system.pg_catalog.pg_database where datname not in ('system','defaultdb','postgres')"
    user_sql = "select usename from system.pg_catalog.pg_user where usename not in ('adminui','root')"
    cluster_settings_sql = (
        "select variable, value from system.crdb_internal.cluster_settings"
    )
    cluster_id_sql = "select * from crdb_internal.cluster_id()"
    version = exec_sql_get(module, cur, version_sql)[0][0]
    node_id = exec_sql_get(module, cur, node_id_sql)[0][0]
    cluster_id = exec_sql_get(module, cur, cluster_id_sql)[0][0]
    cluster_settings = exec_sql_get(module, cur, cluster_settings_sql)
    databases_ = exec_sql_get(module, cur, database_sql)
    users_ = exec_sql_get(module, cur, user_sql)

    db_dict = []
    for d in databases_:
        db_dict.append(d[0])
    user_dict = []
    for u in users_:
        user_dict.append(u[0])

    facts = {"cockroach_version": version.lstrip("v")}
    facts.update({"node_id": node_id})
    facts.update({"cluster_id": cluster_id})
    facts.update({"databases": db_dict})
    facts.update({"dbusers": user_dict})
    facts.update({"cluster_settings": dict(cluster_settings)})

    # Get Cluster settings
    if path:
        license = get_enterprise_license(module, path, host, port, certs_dir)
        facts.update({"enterprise_license": license.split("\n")[1].rstrip("\n")})

    # Get certificate information
    if pyopenssl_exists and certs_dir:
        currdate = datetime.datetime.now()
        cert_dict = {}
        rootcertexpiry = get_cert_expiry_date(clientcert)
        nodecertexpiry = get_cert_expiry_date(nodecert)
        cacertexpiry = get_cert_expiry_date(cacert)
        cert_dict["certificate_information"] = {}
        cert_dict["certificate_information"]["rootcert"] = clientcert
        cert_dict["certificate_information"]["nodecert"] = nodecert
        cert_dict["certificate_information"]["cacert"] = cacert
        cert_dict["certificate_information"]["rootcert_expiration"] = rootcertexpiry
        cert_dict["certificate_information"]["nodecert_expiration"] = nodecertexpiry
        cert_dict["certificate_information"]["cacert_expiration"] = cacertexpiry
        rootdelta = rootcertexpiry - currdate
        nodedelta = nodecertexpiry - currdate
        cadelta = cacertexpiry - currdate
        # module.exit_json(msg=rootdelta.days)
        cert_dict["certificate_information"]["rootcert_expiry_days"] = rootdelta.days
        cert_dict["certificate_information"]["nodecert_expiry_days"] = nodedelta.days
        cert_dict["certificate_information"]["cacert_expiry_days"] = cadelta.days
        facts.update(cert_dict)

    module.exit_json(changed=False, ansible_facts=facts)


from ansible.module_utils.basic import *

if __name__ == "__main__":
    main()
