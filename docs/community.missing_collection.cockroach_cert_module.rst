.. _community.missing_collection.cockroach_cert_module:


*******************************************
community.missing_collection.cockroach_cert
*******************************************

**Manage user certificates in a cockroach cluster**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Manage user certificates in a cockroach cluster




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
                        <div>The name of the user to generate certificate for</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: create a certificate for a user
      cockroach_cert:
        name: user1
        path: "/var/lib/cockroach"




Status
------


Authors
~~~~~~~

- Oscar C, based on the work of Mikael Sandstrom, oravirt@gmail.com, @oravirt
