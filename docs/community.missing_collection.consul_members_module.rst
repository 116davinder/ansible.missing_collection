.. _community.missing_collection.consul_members_module:


*******************************************
community.missing_collection.consul_members
*******************************************

**Get information from Consul (Members).**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information from Consul (Members).



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
                    <b>host</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"localhost"</div>
                </td>
                <td>
                        <div>hostname/ip of consul.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"8500"</div>
                </td>
                <td>
                        <div>port number of consul.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scheme</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>http</b>&nbsp;&larr;</div></li>
                                    <li>https</li>
                        </ul>
                </td>
                <td>
                        <div>http scheme for consul.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>auth token for consul.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get current memebers list
      consul_members:



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
                    <b>result</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>result from the consul api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;Name&#x27;: &#x27;server-1&#x27;, &#x27;Addr&#x27;: &#x27;172.17.0.2&#x27;, &#x27;Port&#x27;: 8301, &#x27;Tags&#x27;: {&#x27;acls&#x27;: &#x27;0&#x27;, &#x27;bootstrap&#x27;: &#x27;1&#x27;, &#x27;build&#x27;: &#x27;1.10.3:c976ffd2&#x27;, &#x27;dc&#x27;: &#x27;dc1&#x27;, &#x27;ft_fs&#x27;: &#x27;1&#x27;, &#x27;ft_si&#x27;: &#x27;1&#x27;, &#x27;id&#x27;: &#x27;61f18701-87ca-2e73-891d-16424997022a&#x27;, &#x27;port&#x27;: &#x27;8300&#x27;, &#x27;raft_vsn&#x27;: &#x27;3&#x27;, &#x27;role&#x27;: &#x27;consul&#x27;, &#x27;segment&#x27;: &#x27;&#x27;, &#x27;vsn&#x27;: &#x27;2&#x27;, &#x27;vsn_max&#x27;: &#x27;3&#x27;, &#x27;vsn_min&#x27;: &#x27;2&#x27;, &#x27;wan_join_port&#x27;: &#x27;8302&#x27;}, &#x27;Status&#x27;: 1, &#x27;ProtocolMin&#x27;: 1, &#x27;ProtocolMax&#x27;: 5, &#x27;ProtocolCur&#x27;: 2, &#x27;DelegateMin&#x27;: 2, &#x27;DelegateMax&#x27;: 5, &#x27;DelegateCur&#x27;: 4}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
