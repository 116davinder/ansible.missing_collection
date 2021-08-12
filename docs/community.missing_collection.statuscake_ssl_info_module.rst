.. _community.missing_collection.statuscake_ssl_info_module:


************************************************
community.missing_collection.statuscake_ssl_info
************************************************

**Get information from Status Cake (SSL).**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information from Status Cake (SSL).
- https://www.statuscake.com/api/v1/#tag/ssl



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
                        <div>api key for statuscake.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>get_all_tests</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>get list of all ssl tests.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>get_one_test</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>fetch info about one specific test <em>id</em>.</div>
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
                        <div>id of ssl test.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.statuscake.com/v1/ssl/"</div>
                </td>
                <td>
                        <div>statuscake ssl api.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get all ssl tests
      community.missing_collection.statuscake_ssl_info:
        api_key: 'Ohxxxxxxxxxxxxxxxxpi'
        get_all_tests: true
      register: __tests

    - name: get info about one ssl test
      community.missing_collection.statuscake_ssl_info:
        api_key: 'Ohxxxxxxxxxxxxxxxxpi'
        get_one_test: true
        id: '{{ __tests.data[0].id }}'



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
                    <b>data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dict/list</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>result of the api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;alert_at&#x27;: [1, 7, 30], &#x27;alert_broken&#x27;: False, &#x27;alert_expiry&#x27;: False, &#x27;alert_mixed&#x27;: False, &#x27;alert_reminder&#x27;: False, &#x27;certificate_score&#x27;: 95, &#x27;certificate_status&#x27;: &#x27;CERT_OK&#x27;, &#x27;check_rate&#x27;: 999999, &#x27;cipher&#x27;: &#x27;TLS_CHACHA20_POLY1305_SHA256&#x27;, &#x27;cipher_score&#x27;: 100, &#x27;contact_groups&#x27;: [], &#x27;flags&#x27;: {&#x27;follow_redirects&#x27;: False, &#x27;has_mixed&#x27;: False, &#x27;has_pfs&#x27;: True, &#x27;is_broken&#x27;: False, &#x27;is_expired&#x27;: False, &#x27;is_extended&#x27;: False, &#x27;is_missing&#x27;: False, &#x27;is_revoked&#x27;: False}, &#x27;follow_redirects&#x27;: False, &#x27;hostname&#x27;: &#x27;new_google_ssl_test&#x27;, &#x27;id&#x27;: &#x27;238191&#x27;, &#x27;issuer_common_name&#x27;: &#x27;GTS CA 1C&#x27;, &#x27;last_reminder&#x27;: 0, &#x27;mixed_content&#x27;: [], &#x27;paused&#x27;: False, &#x27;updated_at&#x27;: &#x27;2021-08-12T20:06:55+00:00&#x27;, &#x27;user_agent&#x27;: &#x27;&#x27;, &#x27;valid_from&#x27;: &#x27;2021-07-12T03:48:00+00:00&#x27;, &#x27;valid_until&#x27;: &#x27;2021-10-04T03:48:00+00:00&#x27;, &#x27;website_url&#x27;: &#x27;https://www.google.com&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
