.. _community.missing_collection.docker_plugins_info_module:


************************************************
community.missing_collection.docker_plugins_info
************************************************

**Get information about Docker Plugins.**


Version added: 0.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get information about Docker Plugins.
- https://docker-py.readthedocs.io/en/stable/plugins.html#



Requirements
------------
The below requirements are needed on the host that executes this module.

- docker


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
                    <b>base_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"unix://var/run/docker.sock"</div>
                </td>
                <td>
                        <div>docker unix sock location.</div>
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
                        <div>id of docker plugin</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: get all plugins
      community.missing_collection.docker_plugins_info:
      register: '__'

    - name: get info about one plugin
      community.missing_collection.docker_plugins_info:
        id: '{{ __.plugins[0].id }}'



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
                    <b>attrs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when success and defined <em>id</em>.</td>
                <td>
                            <div>attributes of given plugin</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;Config&#x27;: {&#x27;Args&#x27;: {&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Name&#x27;: &#x27;&#x27;, &#x27;Settable&#x27;: None, &#x27;Value&#x27;: None}, &#x27;Description&#x27;: &#x27;sshFS plugin for Docker&#x27;, &#x27;DockerVersion&#x27;: &#x27;18.05.0-ce-rc1&#x27;, &#x27;Documentation&#x27;: &#x27;https://docs.docker.com/engine/extend/plugins/&#x27;, &#x27;Entrypoint&#x27;: [&#x27;/docker-volume-sshfs&#x27;], &#x27;Env&#x27;: [{&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Name&#x27;: &#x27;DEBUG&#x27;, &#x27;Settable&#x27;: [&#x27;value&#x27;], &#x27;Value&#x27;: &#x27;0&#x27;}], &#x27;Interface&#x27;: {&#x27;Socket&#x27;: &#x27;sshfs.sock&#x27;, &#x27;Types&#x27;: [&#x27;docker.volumedriver/1.0&#x27;]}, &#x27;IpcHost&#x27;: False, &#x27;Linux&#x27;: {&#x27;AllowAllDevices&#x27;: False, &#x27;Capabilities&#x27;: [&#x27;CAP_SYS_ADMIN&#x27;], &#x27;Devices&#x27;: [{&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Name&#x27;: &#x27;&#x27;, &#x27;Path&#x27;: &#x27;/dev/fuse&#x27;, &#x27;Settable&#x27;: None}]}, &#x27;Mounts&#x27;: [{&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Destination&#x27;: &#x27;/mnt/state&#x27;, &#x27;Name&#x27;: &#x27;state&#x27;, &#x27;Options&#x27;: [&#x27;rbind&#x27;], &#x27;Settable&#x27;: [&#x27;source&#x27;], &#x27;Source&#x27;: &#x27;/var/lib/docker/plugins/&#x27;, &#x27;Type&#x27;: &#x27;bind&#x27;}, {&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Destination&#x27;: &#x27;/root/.ssh&#x27;, &#x27;Name&#x27;: &#x27;sshkey&#x27;, &#x27;Options&#x27;: [&#x27;rbind&#x27;], &#x27;Settable&#x27;: [&#x27;source&#x27;], &#x27;Source&#x27;: &#x27;&#x27;, &#x27;Type&#x27;: &#x27;bind&#x27;}], &#x27;Network&#x27;: {&#x27;Type&#x27;: &#x27;host&#x27;}, &#x27;PidHost&#x27;: False, &#x27;PropagatedMount&#x27;: &#x27;/mnt/volumes&#x27;, &#x27;User&#x27;: {}, &#x27;WorkDir&#x27;: &#x27;&#x27;, &#x27;rootfs&#x27;: {&#x27;diff_ids&#x27;: [&#x27;sha256:ce2b7a99c5db05cfe263bcd3640f2c1ce7c6f4619339633d44e65a8168ec3587&#x27;], &#x27;type&#x27;: &#x27;layers&#x27;}}, &#x27;Enabled&#x27;: True, &#x27;Id&#x27;: &#x27;299f9f87dd9bd0052fb52fa2f5bd6d983b0d7b4f9d505cc07e37742bb17337bd&#x27;, &#x27;Name&#x27;: &#x27;vieux/sshfs:latest&#x27;, &#x27;PluginReference&#x27;: &#x27;docker.io/vieux/sshfs:latest&#x27;, &#x27;Settings&#x27;: {&#x27;Args&#x27;: [], &#x27;Devices&#x27;: [{&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Name&#x27;: &#x27;&#x27;, &#x27;Path&#x27;: &#x27;/dev/fuse&#x27;, &#x27;Settable&#x27;: None}], &#x27;Env&#x27;: [&#x27;DEBUG=0&#x27;], &#x27;Mounts&#x27;: [{&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Destination&#x27;: &#x27;/mnt/state&#x27;, &#x27;Name&#x27;: &#x27;state&#x27;, &#x27;Options&#x27;: [&#x27;rbind&#x27;], &#x27;Settable&#x27;: [&#x27;source&#x27;], &#x27;Source&#x27;: &#x27;/var/lib/docker/plugins/&#x27;, &#x27;Type&#x27;: &#x27;bind&#x27;}, {&#x27;Description&#x27;: &#x27;&#x27;, &#x27;Destination&#x27;: &#x27;/root/.ssh&#x27;, &#x27;Name&#x27;: &#x27;sshkey&#x27;, &#x27;Options&#x27;: [&#x27;rbind&#x27;], &#x27;Settable&#x27;: [&#x27;source&#x27;], &#x27;Source&#x27;: &#x27;&#x27;, &#x27;Type&#x27;: &#x27;bind&#x27;}]}}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>plugins</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when success.</td>
                <td>
                            <div>list of all the docker plugins.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;enabled&#x27;: True, &#x27;id&#x27;: &#x27;299f9f87dd9bd0052fb52fa2f5bd6d983b0d7b4f9d505cc07e37742bb17337bd&#x27;, &#x27;name&#x27;: &#x27;vieux/sshfs:latest&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
