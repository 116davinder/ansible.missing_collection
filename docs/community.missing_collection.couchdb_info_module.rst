.. _community.missing_collection.couchdb_info_module:


*****************************************
community.missing_collection.couchdb_info
*****************************************

**Get information about Couchdb Cluster.**


Version added: 0.1.1

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about Couchdb Cluster.
- https://docs.couchdb.org/en/stable/api/index.html



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
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>all_dbs</b>&nbsp;&larr;</div></li>
                                    <li>active_tasks</li>
                                    <li>membership</li>
                                    <li>scheduler/jobs</li>
                                    <li>scheduler/docs</li>
                                    <li>up</li>
                        </ul>
                </td>
                <td>
                        <div>commands to fetch cluster information.</div>
                </td>
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
                        <div>hostname/ip of couchdb.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>password</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"password"</div>
                </td>
                <td>
                        <div>password for couchdb <em>user</em>.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"5984"</div>
                </td>
                <td>
                        <div>port number of couchdb.</div>
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
                        <div>http scheme for couchdb.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>user</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"admin"</div>
                </td>
                <td>
                        <div>couchdb username.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get list of databases
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'all_dbs'

    - name: get list of active tasks
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'active_tasks'

    - name: get list of nodes in cluster
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'membership'

    - name: get list of scheduled jobs
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'scheduler/jobs'

    - name: get list of scheduler docs
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'scheduler/docs'

    - name: get node status
      community.missing_collection.couchdb_info:
        scheme: 'http'
        host: 'localhost'
        port: '5984'
        user: 'admin'
        password: 'password'
        command: 'up'



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
                    <b>active_tasks</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when command <em>active_tasks</em> is defined and success.</td>
                <td>
                            <div>list of active tasks.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;changes_done&#x27;: 64438, &#x27;database&#x27;: &#x27;mailbox&#x27;, &#x27;pid&#x27;: &#x27;&lt;0.12986.1&gt;&#x27;, &#x27;progress&#x27;: 84, &#x27;started_on&#x27;: 1376116576, &#x27;total_changes&#x27;: 76215, &#x27;type&#x27;: &#x27;database_compaction&#x27;, &#x27;updated_on&#x27;: 1376116619}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>dbs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when command <em>all_dbs</em> is defined and success.</td>
                <td>
                            <div>list of all databases.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;_replicator&#x27;, &#x27;_users&#x27;, &#x27;test&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>docs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when command <em>scheduler/docs</em> is defined and success.</td>
                <td>
                            <div>list of all scheduler docs.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;docs&#x27;: [{&#x27;database&#x27;: &#x27;_replicator&#x27;, &#x27;doc_id&#x27;: &#x27;cdyno-0000001-0000002&#x27;, &#x27;error_count&#x27;: 0, &#x27;id&#x27;: &#x27;e327d79214831ca4c11550b4a453c9ba+continuous&#x27;, &#x27;info&#x27;: {}, &#x27;last_updated&#x27;: &#x27;2017-04-29T05:01:37Z&#x27;, &#x27;node&#x27;: &#x27;node2@127.0.0.1&#x27;, &#x27;source_proxy&#x27;: None, &#x27;target_proxy&#x27;: None, &#x27;source&#x27;: &#x27;http://myserver.com/foo&#x27;, &#x27;start_time&#x27;: &#x27;2017-04-29T05:01:37Z&#x27;, &#x27;state&#x27;: &#x27;running&#x27;, &#x27;target&#x27;: &#x27;http://adm:*****@localhost:15984/cdyno-0000002/&#x27;}], &#x27;offset&#x27;: 0, &#x27;total_rows&#x27;: 1}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>jobs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when command <em>scheduler/jobs</em> is defined and success.</td>
                <td>
                            <div>list of all scheduler jobs.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;jobs&#x27;: [{&#x27;database&#x27;: &#x27;_replicator&#x27;, &#x27;doc_id&#x27;: &#x27;cdyno-0000001-0000003&#x27;, &#x27;history&#x27;: [], &#x27;id&#x27;: &#x27;8f5b1bd0be6f9166ccfd36fc8be8fc22+continuous&#x27;, &#x27;info&#x27;: {}, &#x27;node&#x27;: &#x27;node1@127.0.0.1&#x27;, &#x27;pid&#x27;: &#x27;&lt;0.1850.0&gt;&#x27;, &#x27;source&#x27;: &#x27;http://myserver.com/foo&#x27;, &#x27;start_time&#x27;: &#x27;2017-04-29T05:01:37Z&#x27;, &#x27;target&#x27;: &#x27;http://adm:*****@localhost:15984/cdyno-0000003/&#x27;, &#x27;user&#x27;: None}], &#x27;offset&#x27;: 0, &#x27;total_rows&#x27;: 1}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>membership</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when command <em>membership</em> is defined and success.</td>
                <td>
                            <div>list of members in the cluster.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;all_nodes&#x27;: [&#x27;node1@127.0.0.1&#x27;, &#x27;node2@127.0.0.1&#x27;, &#x27;node3@127.0.0.1&#x27;], &#x27;cluster_nodes&#x27;: [&#x27;node1@127.0.0.1&#x27;, &#x27;node2@127.0.0.1&#x27;, &#x27;node3@127.0.0.1&#x27;]}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>up</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when command <em>up</em> is defined and success.</td>
                <td>
                            <div>status of node.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;status&#x27;: &#x27;ok&#x27;, &#x27;seeds&#x27;: {}}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
