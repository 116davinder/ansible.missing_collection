.. _community.missing_collection.statuscake_pagespeed_info_module:


******************************************************
community.missing_collection.statuscake_pagespeed_info
******************************************************

**Get information from Status Cake (Pagespeed).**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information from Status Cake (Pagespeed).
- https://www.statuscake.com/api/v1/#tag/pagespeed



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
                        <div>get list of all pagespeed tests.</div>
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
                    <b>get_test_histroy</b>
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
                        <div>fetch history info about one specific test <em>id</em>.</div>
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
                        <div>id of pagespeed test.</div>
                        <div>required only for `delete` and `update`.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.statuscake.com/v1/pagespeed/"</div>
                </td>
                <td>
                        <div>statuscake pagespeed api.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get all pagespeed tests
      community.missing_collection.statuscake_pagespeed_info:
        api_key: 'Ohxxxxxxxxxxxxxxxxpi'
        get_all_tests: true
      register: __tests

    - name: get info about one pagespeed test
      community.missing_collection.statuscake_pagespeed_info:
        api_key: 'Ohxxxxxxxxxxxxxxxxpi'
        get_one_test: true
        id: '{{ __tests.data[0].id }}'

    - name: get history about one pagespeed test
      community.missing_collection.statuscake_pagespeed_info:
        api_key: 'Ohxxxxxxxxxxxxxxxxpi'
        get_test_histroy: true
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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;alert_bigger&#x27;: 0, &#x27;alert_slower&#x27;: 0, &#x27;alert_smaller&#x27;: 0, &#x27;check_rate&#x27;: 1440, &#x27;contact_groups&#x27;: [], &#x27;id&#x27;: &#x27;88176&#x27;, &#x27;latest_stats&#x27;: {&#x27;filesize_kb&#x27;: 251.284, &#x27;has_issue&#x27;: False, &#x27;latest_issue&#x27;: &#x27;&#x27;, &#x27;loadtime_ms&#x27;: 344, &#x27;requests&#x27;: 6}, &#x27;location&#x27;: &#x27;PAGESPD-US4&#x27;, &#x27;location_iso&#x27;: &#x27;US&#x27;, &#x27;name&#x27;: &#x27;google_test_new&#x27;, &#x27;paused&#x27;: False, &#x27;website_url&#x27;: &#x27;https://www.google.com&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
