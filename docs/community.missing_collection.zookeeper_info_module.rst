.. _community.missing_collection.zookeeper_info_module:


*******************************************
community.missing_collection.zookeeper_info
*******************************************

**Get Information about Zookeeper Instance.**


Version added: 0.1.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get Information about Zookeeper Instance using Admin Server Rest API.



Requirements
------------
The below requirements are needed on the host that executes this module.

- requests


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
                    <b>command</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>zookeeper admin server command to fetch metrics.</div>
                        <div>{&#x27;example&#x27;: &#x27;stats&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>url of zookeeper admin server.</div>
                        <div>{&#x27;example&#x27;: &#x27;http://localhost:8080&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: fetch list of zookeeper commands
      community.missing_collection.zookeeper_info:
        url: http://localhost:8080

    - name: fetch stats of zookeeper
      community.missing_collection.zookeeper_info:
        url: http://localhost:8080
        command: stats



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>commands</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>when no args and success.</td>
                <td>
                            <div>list of zookeeper admin server commands.</div>
                    <br/>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>output</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when <em>command</em> is defined and success.</td>
                <td>
                            <div>output of given zookeeper admin server command.</div>
                    <br/>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
