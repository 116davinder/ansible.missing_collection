.. _community.missing_collection.rethinkdb_admin_info_module:


*************************************************
community.missing_collection.rethinkdb_admin_info
*************************************************

**Get information from RethinkDB Database.**


Version added: 0.2.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information from RethinkDB Database.
- https://rethinkdb.com/docs/system-tables/#overview



Requirements
------------
The below requirements are needed on the host that executes this module.

- rethinkdb


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
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>hostname of rethinkdb.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">10</div>
                </td>
                <td>
                        <div>limit number of results to fetch.</div>
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
                        <b>Default:</b><br/><div style="color: blue">""</div>
                </td>
                <td>
                        <div>password for rethinkdb <em>user</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>port</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">28015</div>
                </td>
                <td>
                        <div>port number of rethinkdb.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ssl</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"None"</div>
                </td>
                <td>
                        <div>use SSL for rethinkdb connection.</div>
                        <div>may not work!.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>table</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>table_config</li>
                                    <li>server_config</li>
                                    <li>db_config</li>
                                    <li>cluster_config</li>
                                    <li>table_status</li>
                                    <li><div style="color: blue"><b>server_status</b>&nbsp;&larr;</div></li>
                                    <li>current_issues</li>
                                    <li>users</li>
                                    <li>permissions</li>
                                    <li>jobs</li>
                                    <li>stats</li>
                                    <li>logs</li>
                        </ul>
                </td>
                <td>
                        <div>name of the system table.</div>
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
                        <div>rethinkdb username.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get server status from rethinkdb
      community.missing_collection.rethinkdb_admin_info:
        host: 'localhost'
        port: 28015
        user: 'admin'
        password: ''
        table: 'server_status'

    - name: get user list from rethinkdb
      community.missing_collection.rethinkdb_admin_info:
        host: 'localhost'
        port: 28015
        user: 'admin'
        password: ''
        table: 'users'



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
                            <div>result of the database query.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;id&#x27;: &#x27;f3389b47-3a78-4108-b85e-45cd06bcc69a&#x27;, &#x27;name&#x27;: &#x27;555e32d208e5_mgu&#x27;, &#x27;network&#x27;: {&#x27;canonical_addresses&#x27;: [{&#x27;host&#x27;: &#x27;127.0.0.1&#x27;, &#x27;port&#x27;: 29015}, {&#x27;host&#x27;: &#x27;172.17.0.2&#x27;, &#x27;port&#x27;: 29015}], &#x27;cluster_port&#x27;: 29015, &#x27;connected_to&#x27;: {}, &#x27;hostname&#x27;: &#x27;555e32d208e5&#x27;, &#x27;http_admin_port&#x27;: 8080, &#x27;reql_port&#x27;: 28015, &#x27;time_connected&#x27;: &#x27;2021-07-20T16:35:58.725000+00:00&#x27;}, &#x27;process&#x27;: {&#x27;argv&#x27;: [&#x27;rethinkdb&#x27;, &#x27;--bind&#x27;, &#x27;all&#x27;], &#x27;cache_size_mb&#x27;: 11712.3125, &#x27;pid&#x27;: 1, &#x27;time_started&#x27;: &#x27;2021-07-20T16:35:58.723000+00:00&#x27;, &#x27;version&#x27;: &#x27;rethinkdb 2.4.1~0buster (CLANG 7.0.1 (tags/RELEASE_701/final))&#x27;}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
