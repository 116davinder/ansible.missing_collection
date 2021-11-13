.. _community.missing_collection.cockroach_cluster_module:


**********************************************
community.missing_collection.cockroach_cluster
**********************************************

**Manage a cockroach cluster**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage a cockroach cluster




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
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                <td>
                        <div>The name of the service</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

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




Status
------


Authors
~~~~~~~

- Mikael Sandström, oravirt@gmail.com, @oravirt
