.. _community.missing_collection.checkly_checks_info_module:


************************************************
community.missing_collection.checkly_checks_info
************************************************

**Get information about checkly checks.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about checkly checks.
- https://www.checklyhq.com/docs/api#tag/Checks



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
                    <b>api_check_url_filter_pattern</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Filters the results by a string contained in the URL of an API check.</div>
                        <div>for instance a domain like <b>www.myapp.com</b>.</div>
                        <div>Only returns API checks.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>api_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>api key for checkly.</div>
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
                        <div>id of alert channel.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>limit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">100</div>
                </td>
                <td>
                        <div>number of checks in one call.</div>
                </td>
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
                        <div>page number of retrieve call.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.checklyhq.com/v1/checks/"</div>
                </td>
                <td>
                        <div>checkly api.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get all checks from checkly
      community.missing_collection.checkly_checks_info:
        api_key: 'a8f08873c494445ba156e572e1324300'

    - name: get one check from checkly
      community.missing_collection.checkly_checks_info:
        api_key: 'a8f08873c494445ba156e572e1324300'
        id: '39308'



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
                      <span style="color: purple">list/dict</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>result of checkly api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;id&#x27;: &#x27;string&#x27;, &#x27;name&#x27;: &#x27;string&#x27;, &#x27;checkType&#x27;: &#x27;BROWSER&#x27;, &#x27;frequency&#x27;: 10, &#x27;frequencyOffset&#x27;: 1, &#x27;activated&#x27;: True, &#x27;muted&#x27;: False, &#x27;doubleCheck&#x27;: True, &#x27;sslCheck&#x27;: True, &#x27;shouldFail&#x27;: True, &#x27;locations&#x27;: [], &#x27;request&#x27;: {}, &#x27;script&#x27;: &#x27;string&#x27;, &#x27;environmentVariables&#x27;: [], &#x27;tags&#x27;: [], &#x27;setupSnippetId&#x27;: 0, &#x27;tearDownSnippetId&#x27;: 0, &#x27;localSetupScript&#x27;: &#x27;string&#x27;, &#x27;localTearDownScript&#x27;: &#x27;string&#x27;, &#x27;alertSettings&#x27;: {}, &#x27;useGlobalAlertSettings&#x27;: True, &#x27;degradedResponseTime&#x27;: 10000, &#x27;maxResponseTime&#x27;: 20000, &#x27;groupId&#x27;: 0, &#x27;groupOrder&#x27;: 0, &#x27;runtimeId&#x27;: &#x27;2021.06&#x27;, &#x27;alertChannelSubscriptions&#x27;: [], &#x27;alertChannels&#x27;: {}, &#x27;created_at&#x27;: &#x27;2019-08-24&#x27;, &#x27;updated_at&#x27;: &#x27;2019-08-24T14:15:22Z&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
