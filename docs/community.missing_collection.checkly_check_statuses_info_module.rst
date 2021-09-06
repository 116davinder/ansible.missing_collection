.. _community.missing_collection.checkly_check_statuses_info_module:


********************************************************
community.missing_collection.checkly_check_statuses_info
********************************************************

**Get information from checkly about check statuses.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information from checkly about check statuses.
- https://www.checklyhq.com/docs/api#tag/Check-status



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
                    <b>id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>check id.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.checklyhq.com/v1/check-statuses/"</div>
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

    - name: get details of all checkly check statuses
      community.missing_collection.checkly_check_statuses_info:
        api_key: 'a8f0xxxxxxxxxxx00'
      register: __

    - name: get details of one specific check statuses
      community.missing_collection.checkly_check_statuses_info:
        api_key: 'a8f0xxxxxxxxxxx00'
        id: '{{ __.data[0].checkId }}'



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;name&#x27;: &#x27;string&#x27;, &#x27;checkId&#x27;: &#x27;string&#x27;, &#x27;hasFailures&#x27;: True, &#x27;hasErrors&#x27;: True, &#x27;isDegraded&#x27;: True, &#x27;longestRun&#x27;: 0, &#x27;shortestRun&#x27;: 0, &#x27;lastRunLocation&#x27;: &#x27;string&#x27;, &#x27;lastCheckRunId&#x27;: &#x27;string&#x27;, &#x27;sslDaysRemaining&#x27;: 0, &#x27;created_at&#x27;: &#x27;2019-08-24&#x27;, &#x27;updated_at&#x27;: &#x27;2019-08-24T14:15:22Z&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
