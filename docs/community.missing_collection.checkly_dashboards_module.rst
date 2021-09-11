.. _community.missing_collection.checkly_dashboards_module:


***********************************************
community.missing_collection.checkly_dashboards
***********************************************

**Management of the checkly Dashboards.**


Version added: 0.3.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Management of the checkly Dashboards.
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
                        <div>type of operation on dashboards.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>custom_domain</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A custom user domain, e.g. &quot;status.example.com&quot;.</div>
                        <div>See the docs on updating your DNS and SSL usage.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>custom_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A subdomain name under &quot;checklyhq.com&quot;.</div>
                        <div>Needs to be unique across all users.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>header</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"Managed by Ansible Automation"</div>
                </td>
                <td>
                        <div>A piece of text displayed at the top of your dashboard.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>hide_tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>Show or hide the tags on the dashboard.</div>
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
                        <div>required only for <em>delete</em> and <em>update</em>.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>logo</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A URL pointing to an image file.</div>
                        <div>example <em>https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png</em></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>paginate</b>
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
                        <div>Determines of pagination is on or off.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>pagination_rate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>30</li>
                                    <li><div style="color: blue"><b>60</b>&nbsp;&larr;</div></li>
                                    <li>300</li>
                        </ul>
                </td>
                <td>
                        <div>How often to trigger pagination in seconds.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>refresh_rate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>60</b>&nbsp;&larr;</div></li>
                                    <li>300</li>
                                    <li>600</li>
                        </ul>
                </td>
                <td>
                        <div>How often to refresh the dashboard in seconds.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tags</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>A list of one or more tags that filter which checks to display on the dashboard.</div>
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
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>width</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>FULL</b>&nbsp;&larr;</div></li>
                                    <li>960PX</li>
                        </ul>
                </td>
                <td>
                        <div>Determines whether to use the full screen or focus in the center.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: create a dashboard
      community.missing_collection.checkly_dashboards:
        api_key: '4a7734debb54464e9fefe8b4f14b896e'
        command: 'create'
        custom_domain: '6605c28f.axway.com'
        custom_url: "6605c28f"
        header: 'Managed by Ansible Automation'
        tags:
          - 'api'
          - 'axway'
        logo: 'https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png'
      register: __

    - name: update a dashboard
      community.missing_collection.checkly_dashboards:
        api_key: '4a7734debb54464e9fefe8b4f14b896e'
        command: 'update'
        custom_domain: '6605c28f.axway.com'
        custom_url: "6605c28f"
        header: 'Managed by Ansible Automation'
        tags:
          - 'api'
          - 'axway'
        id: '{{ __.result.dashboardId }}'
        logo: 'https://upload.wikimedia.org/wikipedia/en/8/8a/Axway_Software_logo_June_2017.png'

    - name: delete a dashboard
      community.missing_collection.checkly_dashboards:
        api_key: '4a7734debb54464e9fefe8b4f14b896e'
        command: 'delete'
        id: '{{ __.result.dashboardId }}'



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
                            <div>result of checkly api.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;customUrl&#x27;: &#x27;string&#x27;, &#x27;customDomain&#x27;: &#x27;string&#x27;, &#x27;logo&#x27;: &#x27;string&#x27;, &#x27;header&#x27;: &#x27;string&#x27;, &#x27;width&#x27;: &#x27;FULL&#x27;, &#x27;refreshRate&#x27;: 60, &#x27;paginate&#x27;: True, &#x27;paginationRate&#x27;: 30, &#x27;tags&#x27;: [], &#x27;hideTags&#x27;: False, &#x27;dashboardId&#x27;: &#x27;string&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
