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




Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
