.. _community.missing_collection.checkly_dashboards_info_module:


****************************************************
community.missing_collection.checkly_dashboards_info
****************************************************

**Get information about checkly dashboards.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about checkly dashboards.
- https://www.checklyhq.com/docs/api#tag/Dashboards



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
                        <div>id of dashboard.</div>
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
                        <div>number of dashboards retrieved in one call.</div>
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
                        <div>page number of dashboards retrieve call.</div>
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
                        <b>Default:</b><br/><div style="color: blue">"https://api.checklyhq.com/v1/dashboards/"</div>
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

    - name: get all dashboards from checkly
      community.missing_collection.checkly_dashboards_info:
        api_key: 'a8f08873c494445ba156e572e1324300'

    - name: get one dashboard from checkly
      community.missing_collection.checkly_dashboards_info:
        api_key: 'a8f08873c494445ba156e572e1324300'
        id: 'bfffd643'



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
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;customUrl&#x27;: &#x27;string&#x27;, &#x27;customDomain&#x27;: &#x27;string&#x27;, &#x27;logo&#x27;: &#x27;string&#x27;, &#x27;header&#x27;: &#x27;string&#x27;, &#x27;width&#x27;: &#x27;FULL&#x27;, &#x27;refreshRate&#x27;: 60, &#x27;paginate&#x27;: True, &#x27;paginationRate&#x27;: 30, &#x27;tags&#x27;: [], &#x27;hideTags&#x27;: False, &#x27;dashboardId&#x27;: &#x27;string&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
