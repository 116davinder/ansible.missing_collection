.. _community.missing_collection.cockroach_facts_module:


********************************************
community.missing_collection.cockroach_facts
********************************************

**Returns facts about a Cockroach Cluster**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Returns facts about a Cockroach Cluster



Requirements
------------
The below requirements are needed on the host that executes this module.

- psycopg2


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>certs_dir</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Path to certificates on the cluster host</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"localhost"</div>
                </td>
                <td>
                        <div>The cluster host</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">26257</div>
                </td>
                <td>
                        <div>The cluster port</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"root"</div>
                </td>
                <td>
                        <div>The cluster user to connect as</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - psycopg2 needs to be installed



Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Mikael Sandström, oravirt@gmail.com, @oravirt
