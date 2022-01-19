.. _community.missing_collection.doh_module:


********************************
community.missing_collection.doh
********************************

**DNS Lookup over HTTPS.**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- DNS Lookup over HTTPS from various Public DOH Servers like Google/Cloudflare/Quad9/Alibaba.
- https://developers.cloudflare.com/1.1.1.1/encrypted-dns/dns-over-https/make-api-requests/dns-json
- https://developers.google.com/speed/public-dns/docs/doh/json
- https://www.quad9.net/news/blog/doh-with-quad9-dns-servers/
- https://www.alibabacloud.com/help/en/doc-detail/171666.html



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
                    <b>cd</b>
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
                        <div>set to disable validation.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>do</b>
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
                        <div>set if client wants DNSSEC data.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>domain_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>domain name or hostname for lookup.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>google</li>
                                    <li><div style="color: blue"><b>cloudflare</b>&nbsp;&larr;</div></li>
                                    <li>quad9</li>
                                    <li>alibaba</li>
                        </ul>
                </td>
                <td>
                        <div>DNS over HTTPS can be queried from Google/Cloudflare/Quad9.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"A"</div>
                </td>
                <td>
                        <div>type of dns lookup.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: fetch A record from cloudflare DNS over HTTPS
      community.missing_collection.doh:
        source: "cloudflare"
        domain_name: "example.com"
        type: "A"

    - name: fetch NS record from Google DNS over HTTPS
      community.missing_collection.doh:
        source: "google"
        name: "example.com"
        type: "NS"

    - name: fetch mail record from Quad9 DNS over HTTPS
      community.missing_collection.doh:
        source: "quad9"
        name: "example.com"
        type: "MX"

    - name: fetch A record from Alibaba DNS over HTTPS
      community.missing_collection.doh:
        source: "alibaba"
        name: "example.com"
        type: "A"



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
                            <div>result of the api request.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;Status&#x27;: 0, &#x27;TC&#x27;: False, &#x27;RD&#x27;: True, &#x27;RA&#x27;: True, &#x27;AD&#x27;: True, &#x27;CD&#x27;: False, &#x27;Question&#x27;: [{&#x27;name&#x27;: &#x27;example.com.&#x27;, &#x27;type&#x27;: 28}], &#x27;Answer&#x27;: [{&#x27;name&#x27;: &#x27;example.com.&#x27;, &#x27;type&#x27;: 28, &#x27;TTL&#x27;: 1726, &#x27;data&#x27;: &#x27;2606:2800:220:1:248:1893:25c8:1946&#x27;}]}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
