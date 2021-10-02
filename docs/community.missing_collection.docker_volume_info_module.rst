.. _community.missing_collection.docker_volume_info_module:


***********************************************
community.missing_collection.docker_volume_info
***********************************************

**Get information about Docker Volumes.**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about Docker Volumes.
- https://docker-py.readthedocs.io/en/stable/volumes.html#



Requirements
------------
The below requirements are needed on the host that executes this module.

- docker


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
                    <b>base_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"unix://var/run/docker.sock"</div>
                </td>
                <td>
                        <div>docker unix sock location.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>id of docker volume</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get all volumes
      community.missing_collection.docker_volume_info:
      register: '__'

    - name: get info about one volume
      community.missing_collection.docker_volume_info:
        id: '{{ __.volumes[0].id }}'



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
                    <b>attrs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when success and defined <em>id</em>.</td>
                <td>
                            <div>attributes of given volume</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;CreatedAt&#x27;: &#x27;2021-09-23T21:01:17Z&#x27;, &#x27;Driver&#x27;: &#x27;local&#x27;, &#x27;Labels&#x27;: None, &#x27;Mountpoint&#x27;: &#x27;/var/lib/docker/volumes/34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02/_data&#x27;, &#x27;Name&#x27;: &#x27;34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02&#x27;, &#x27;Options&#x27;: None, &#x27;Scope&#x27;: &#x27;local&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>volumes</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>list of all the docker volumes.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;id&#x27;: &#x27;34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02&#x27;, &#x27;name&#x27;: &#x27;34a961a26cd0cb99cdb2e5912b28f02f3460081590243067d1c6cedf50cb8e02&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
