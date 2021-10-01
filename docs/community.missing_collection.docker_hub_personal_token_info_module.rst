.. _community.missing_collection.docker_hub_personal_token_info_module:


***********************************************************
community.missing_collection.docker_hub_personal_token_info
***********************************************************

**Get information about docker hub personal tokens.**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about docker hub personal tokens.
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
                    <b>page</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">1</div>
                </td>
                <td>
                        <div>page number of personal tokens retrieve call.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>page_size</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">100</div>
                </td>
                <td>
                        <div>number of personal tokens retrieved in one call.</div>
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
                        <div>jwt/Bearer token for docker hub api.</div>
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
                        <div>docker hub api.</div>
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
                        <div>if defined, will fetch info about given <em>uuid</em> persona token only.</div>
                        <div>else all personal tokens will be fetched.</div>
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

    - name: get information about all personal tokens
      community.missing_collection.docker_hub_personal_token_info:
        token: '{{ __.token }}'
      register: '__all'

    - name: get information about one personal tokens
      community.missing_collection.docker_hub_personal_token_info:
        token: '{{ __.token }}'
        uuid: '{{ __all.result.results[0].uuid }}'



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
                <td>when success.</td>
                <td>
                            <div>result of docker hub api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;count&#x27;: 1, &#x27;next&#x27;: &#x27;string&#x27;, &#x27;previous&#x27;: &#x27;string&#x27;, &#x27;active_count&#x27;: 1, &#x27;results&#x27;: [{&#x27;uuid&#x27;: &#x27;b30bbf97-506c-4ecd-aabc-842f3cb484fb&#x27;, &#x27;client_id&#x27;: &#x27;HUB&#x27;, &#x27;creator_ip&#x27;: &#x27;127.0.0.1&#x27;, &#x27;creator_ua&#x27;: &#x27;some user agent&#x27;, &#x27;created_at&#x27;: &#x27;2021-07-20T12:00:00.000Z&#x27;, &#x27;last_used&#x27;: &#x27;string&#x27;, &#x27;generated_by&#x27;: &#x27;manual&#x27;, &#x27;is_active&#x27;: True, &#x27;token&#x27;: &#x27;&#x27;, &#x27;token_label&#x27;: &#x27;My read only token&#x27;, &#x27;scopes&#x27;: [&#x27;repo:read&#x27;]}]}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
