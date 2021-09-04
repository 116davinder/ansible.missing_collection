.. _community.missing_collection.checkly_reporting_info_module:


***************************************************
community.missing_collection.checkly_reporting_info
***************************************************

**Generates a report with aggregate statistics for checks and check groups.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Generates a report with aggregate statistics for checks and check groups.
- https://www.checklyhq.com/docs/api#tag/Reporting



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
                        <div>api key for checkly.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>deactivated</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Filter checks by activated status.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filter_by_tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>Use tags to filter the checks you want to see in your report.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>from_date</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>unix epoch from date to filter results.</div>
                        <div>Setting a custom <em>from_date</em> timestamp overrides the use of any <em>preset_window</em>.</div>
                        <div>check example for format or use <em>to_datetime</em> filter.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>preset_window</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>last24Hrs</b>&nbsp;&larr;</div></li>
                                    <li>last7Days</li>
                                    <li>last30Days</li>
                                    <li>thisWeek</li>
                                    <li>thisMonth</li>
                                    <li>lastWeek</li>
                                    <li>lastMonth</li>
                        </ul>
                </td>
                <td>
                        <div>Preset reporting windows are used for quickly generating report on commonly used windows.</div>
                        <div>Can be overridden by using a custom <em>to_date</em> and <em>from_date</em> timestamp.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>to_date</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>unix epoch to date to filter results.</div>
                        <div>Setting a custom <em>to_date</em> timestamp overrides the use of any <em>preset_window</em>.</div>
                        <div>check example for format or use <em>to_datetime</em> filter.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.checklyhq.com/v1/reporting"</div>
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

    - name: generate report for last 24 hours
      community.missing_collection.checkly_reporting_info:
        api_key: '95e3814891ef433298150a539750076e'
        preset_window: 'last24Hrs'

    - name: generate report for specific period
      community.missing_collection.checkly_reporting_info:
        api_key: '95e3814891ef433298150a539750076e'
        from_date: "{{ ('2021-09-02 06:50:00'|to_datetime).strftime('%s') }}"
        to_date: "{{ ('2021-09-04 06:50:00'|to_datetime).strftime('%s') }}"



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
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>result of the api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;name&#x27;: &#x27;string&#x27;, &#x27;checkId&#x27;: &#x27;string&#x27;, &#x27;checkType&#x27;: &#x27;string&#x27;, &#x27;deactivated&#x27;: True, &#x27;tags&#x27;: [&#x27;string&#x27;], &#x27;aggregate&#x27;: {&#x27;successRatio&#x27;: 0, &#x27;avg&#x27;: 0, &#x27;p95&#x27;: 0, &#x27;p99&#x27;: 0}}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
