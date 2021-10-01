.. _community.missing_collection.docker_hub_personal_token_module:


******************************************************
community.missing_collection.docker_hub_personal_token
******************************************************

**Management of the Docker Hub Personal Tokens.**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Management of the Docker Hub Personal Tokens.
- https://docs.docker.com/docker-hub/api/latest/#tag/access-tokens



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
                                    <li><div style="color: blue"><b>create</b>&nbsp;&larr;</div></li>
                                    <li>update</li>
                                    <li>delete</li>
                        </ul>
                </td>
                <td>
                        <div>type of operation on docker hub api.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>is_active</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>enable/disable personal token.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>scopes</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Valid scopes &quot;repo:admin&quot;, &quot;repo:write&quot;, &quot;repo:read&quot;, &quot;repo:public_read&quot;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>jwt/bearer token for api.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>token_label</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Friendly name for you to identify the token.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"https://hub.docker.com/v2/access-tokens/"</div>
                </td>
                <td>
                        <div>docker hub personal token api.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>uuid</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>uuid of personal token.</div>
                        <div>required only for command <em>delete</em>/<em>update</em>.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get jwt token from docker hub
      community.missing_collection.docker_hub_token:
        username: 'testUser'
        password: 'aDL0xxxxxxxxxxoQt6'
      register: '__'

    - name: create docker hub personal token
      community.missing_collection.docker_hub_personal_token:
        token: '{{ __.token }}'
        command: 'create'
        token_label: 'Ansible Managed Token'
        scopes:
          - 'repo:admin'
      register: '__created'

    - name: update docker hub personal token aka disable it.
      community.missing_collection.docker_hub_personal_token:
        token: '{{ __.token }}'
        command: 'update'
        uuid: '{{ __created.result["uuid"] }}'
        is_active: false

    - name: delete docker hub personal token.
      community.missing_collection.docker_hub_personal_token:
        token: '{{ __.token }}'
        command: 'delete'
        uuid: '{{ __created.result["uuid"] }}'



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
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when command is <em>create</em>/<em>update</em> and success.</td>
                <td>
                            <div>result of docker hub api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;uuid&#x27;: &#x27;b30bbf97-506c-4ecd-aabc-842f3cb484fb&#x27;, &#x27;client_id&#x27;: &#x27;HUB&#x27;, &#x27;creator_ip&#x27;: &#x27;127.0.0.1&#x27;, &#x27;creator_ua&#x27;: &#x27;some user agent&#x27;, &#x27;created_at&#x27;: &#x27;2021-07-20T12:00:00.000Z&#x27;, &#x27;last_used&#x27;: &#x27;string&#x27;, &#x27;generated_by&#x27;: &#x27;manual&#x27;, &#x27;is_active&#x27;: True, &#x27;token&#x27;: &#x27;a7a5ef25-8889-43a0-8cc7-f2a94268e861&#x27;, &#x27;token_label&#x27;: &#x27;My read only token&#x27;, &#x27;scopes&#x27;: [&#x27;repo:read&#x27;]}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
