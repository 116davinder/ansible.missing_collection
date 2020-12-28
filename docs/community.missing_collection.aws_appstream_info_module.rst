.. _community.missing_collection.aws_appstream_info_module:


***********************************************
community.missing_collection.aws_appstream_info
***********************************************

**Get details about Amazon AppStream 2.0.**


Version added: 0.0.2

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get Information about Amazon AppStream 2.0 API.
- https://docs.aws.amazon.com/appstream2/latest/APIReference/API_Operations.html



Requirements
------------
The below requirements are needed on the host that executes this module.

- boto
- boto3
- botocore
- python >= 2.6


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
                    <b>authentication_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>API</li>
                                    <li>SAML</li>
                                    <li><div style="color: blue"><b>USERPOOL</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>what type of authentication for <em>describe_user</em>?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>aws_access_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AWS access key. If not set then the value of the AWS_ACCESS_KEY_ID, AWS_ACCESS_KEY or EC2_ACCESS_KEY environment variable is used.</div>
                        <div>If <em>profile</em> is set this parameter is ignored.</div>
                        <div>Passing the <em>aws_access_key</em> and <em>profile</em> options at the same time has been deprecated and the options will be made mutually exclusive after 2022-06-01.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: ec2_access_key, access_key</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>aws_ca_bundle</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The location of a CA Bundle to use when validating SSL certificates.</div>
                        <div>Only used for boto3 based modules.</div>
                        <div>Note: The CA Bundle is read &#x27;module&#x27; side and may need to be explicitly copied from the controller if not run locally.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>aws_config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>A dictionary to modify the botocore configuration.</div>
                        <div>Parameters can be found at <a href='https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html#botocore.config.Config'>https://botocore.amazonaws.com/v1/documentation/api/latest/reference/config.html#botocore.config.Config</a>.</div>
                        <div>Only the &#x27;user_agent&#x27; key is used for boto modules. See <a href='http://boto.cloudhackers.com/en/latest/boto_config_tut.html#boto'>http://boto.cloudhackers.com/en/latest/boto_config_tut.html#boto</a> for more boto configuration.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>aws_secret_key</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AWS secret key. If not set then the value of the AWS_SECRET_ACCESS_KEY, AWS_SECRET_KEY, or EC2_SECRET_KEY environment variable is used.</div>
                        <div>If <em>profile</em> is set this parameter is ignored.</div>
                        <div>Passing the <em>aws_secret_key</em> and <em>profile</em> options at the same time has been deprecated and the options will be made mutually exclusive after 2022-06-01.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: ec2_secret_key, secret_key</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>debug_botocore_endpoint_logs</b>
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
                        <div>Use a botocore.endpoint logger to parse the unique (rather than total) &quot;resource:action&quot; API calls made during a task, outputing the set to the resource_actions key in the task results. Use the aws_resource_action callback to output to total list made during a playbook. The ANSIBLE_DEBUG_BOTOCORE_LOGS environment variable may also be used.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_directory_configs</b>
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
                        <div>do you want to describe all appstreams directory configs or given <em>names</em> of directory configs?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_fleets</b>
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
                        <div>do you want to describe all appstreams fleet or given <em>names</em> of fleets?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_image_builders</b>
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
                        <div>do you want to describe all appstreams image builders or given <em>names</em> of builders?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_images</b>
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
                        <div>do you want to describe all appstreams images or given <em>names</em> of images?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_users</b>
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
                        <div>do you want to describe appstreams user or given <em>authentication_type</em>?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>ec2_url</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Url to use to connect to EC2 or your Eucalyptus cloud (by default the module will use EC2 endpoints). Ignored for modules where region is required. Must be specified for all other modules if region is not used. If not set then the value of the EC2_URL environment variable, if any, is used.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: aws_endpoint_url, endpoint_url</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>image_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>PUBLIC</b>&nbsp;&larr;</div></li>
                                    <li>PRIVATE</li>
                                    <li>SHARED</li>
                        </ul>
                </td>
                <td>
                        <div>what type of image will be decribed?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>names</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">[]</div>
                </td>
                <td>
                        <div>can be names of the fleets to describe?</div>
                        <div>can be names of the stacks to describe?</div>
                        <div>can be aws app stream directory names to describe?</div>
                        <div>can be names of the image builders to describe?</div>
                        <div>can be names of the public or private images to describe?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>profile</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Uses a boto profile. Only works with boto &gt;= 2.24.0.</div>
                        <div>Using <em>profile</em> will override <em>aws_access_key</em>, <em>aws_secret_key</em> and <em>security_token</em> and support for passing them at the same time as <em>profile</em> has been deprecated.</div>
                        <div><em>aws_access_key</em>, <em>aws_secret_key</em> and <em>security_token</em> will be made mutually exclusive with <em>profile</em> after 2022-06-01.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: aws_profile</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>region</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The AWS region to use. If not specified then the value of the AWS_REGION or EC2_REGION environment variable, if any, is used. See <a href='http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region'>http://docs.aws.amazon.com/general/latest/gr/rande.html#ec2_region</a></div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: aws_region, ec2_region</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>security_token</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>AWS STS security token. If not set then the value of the AWS_SECURITY_TOKEN or EC2_SECURITY_TOKEN environment variable is used.</div>
                        <div>If <em>profile</em> is set this parameter is ignored.</div>
                        <div>Passing the <em>security_token</em> and <em>profile</em> options at the same time has been deprecated and the options will be made mutually exclusive after 2022-06-01.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: aws_security_token, access_token</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate_certs</b>
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
                        <div>When set to &quot;no&quot;, SSL certificates will not be validated for boto versions &gt;= 2.6.0.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - If parameters are not set within the module, the following environment variables can be used in decreasing order of precedence ``AWS_URL`` or ``EC2_URL``, ``AWS_PROFILE`` or ``AWS_DEFAULT_PROFILE``, ``AWS_ACCESS_KEY_ID`` or ``AWS_ACCESS_KEY`` or ``EC2_ACCESS_KEY``, ``AWS_SECRET_ACCESS_KEY`` or ``AWS_SECRET_KEY`` or ``EC2_SECRET_KEY``, ``AWS_SECURITY_TOKEN`` or ``EC2_SECURITY_TOKEN``, ``AWS_REGION`` or ``EC2_REGION``, ``AWS_CA_BUNDLE``
   - Ansible uses the boto configuration file (typically ~/.boto) if no credentials are provided. See https://boto.readthedocs.io/en/latest/boto_config_tut.html
   - ``AWS_REGION`` or ``EC2_REGION`` can be typically be used to specify the AWS region, when required, but this can also be configured in the boto config file



Examples
--------

.. code-block:: yaml

    - name: "describe all fleets of aws app streams"
      aws_appstream_info:
        describe_fleets: true

    - name: "describe all directory configs of aws app streams"
      aws_appstream_info:
        describe_directory_configs: true

    - name: "describe all image builder of aws app streams"
      aws_appstream_info:
        describe_image_builders: true

    - name: "describe all images of aws app streams"
      aws_appstream_info:
        describe_images: true
        image_type: 'PRIVATE'

    - name: "describe all users of aws app streams"
      aws_appstream_info:
        describe_users: true
        authentication_type: 'USERPOOL'



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
                    <b>directory_configs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `names` and `describe_directory_configs` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified Directory Config objects for AppStream 2.0, if the names for these objects are provided.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;directory_name&#x27;: &#x27;string&#x27;, &#x27;organizational_unit_distinguished_names&#x27;: [], &#x27;service_account_credentials&#x27;: {}, &#x27;created_time&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>fleets</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `names` and `describe_fleets` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified fleets, if the fleet names are provided.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;arn&#x27;: &#x27;string&#x27;, &#x27;name&#x27;: &#x27;string&#x27;, &#x27;display_name&#x27;: &#x27;string&#x27;, &#x27;description&#x27;: &#x27;string&#x27;, &#x27;image_name&#x27;: &#x27;string&#x27;, &#x27;image_arn&#x27;: &#x27;string&#x27;, &#x27;instance_type&#x27;: &#x27;string&#x27;, &#x27;fleet_type&#x27;: &#x27;ALWAYS_ON&#x27;, &#x27;compute_capacity_status&#x27;: {}, &#x27;max_user_duration_in_seconds&#x27;: 123, &#x27;disconnect_timeout_in_seconds&#x27;: 123, &#x27;state&#x27;: &#x27;STARTING&#x27;, &#x27;vpc_config&#x27;: {}, &#x27;created_time&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;fleet_errors&#x27;: [], &#x27;enable_default_internet_access&#x27;: True, &#x27;domain_join_info&#x27;: {}, &#x27;idle_disconnect_timeout_in_seconds&#x27;: 123, &#x27;iam_role_arn&#x27;: &#x27;string&#x27;, &#x27;stream_view&#x27;: &#x27;APP&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>image_builders</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `names` and `describe_image_builders` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified image builders, if the image builder names are provided.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;name&#x27;: &#x27;string&#x27;, &#x27;arn&#x27;: &#x27;string&#x27;, &#x27;image_arn&#x27;: &#x27;string&#x27;, &#x27;description&#x27;: &#x27;string&#x27;, &#x27;display_name&#x27;: &#x27;string&#x27;, &#x27;vpc_config&#x27;: {}, &#x27;instance_type&#x27;: &#x27;string&#x27;, &#x27;platform&#x27;: &#x27;WINDOWS&#x27;, &#x27;iam_role_arn&#x27;: &#x27;string&#x27;, &#x27;state&#x27;: &#x27;PENDING&#x27;, &#x27;state_change_reason&#x27;: {}, &#x27;created_time&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;enable_default_internet_access&#x27;: True, &#x27;domain_join_info&#x27;: {}, &#x27;network_access_configuration&#x27;: {}, &#x27;image_builder_errors&#x27;: [], &#x27;appstream_agent_version&#x27;: &#x27;string&#x27;, &#x27;access_endpoints&#x27;: []}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>images</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `names` and `describe_images` and `image_type` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified images, if the image names are provided.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;name&#x27;: &#x27;string&#x27;, &#x27;arn&#x27;: &#x27;string&#x27;, &#x27;base_image_arn&#x27;: &#x27;string&#x27;, &#x27;display_name&#x27;: &#x27;string&#x27;, &#x27;state&#x27;: &#x27;PENDING&#x27;, &#x27;visibility&#x27;: &#x27;PUBLIC&#x27;, &#x27;image_builder_supported&#x27;: &#x27;True|False&#x27;, &#x27;image_builder_name&#x27;: &#x27;string&#x27;, &#x27;platform&#x27;: &#x27;WINDOWS&#x27;, &#x27;description&#x27;: &#x27;string&#x27;, &#x27;state_change_reason&#x27;: {}, &#x27;applications&#x27;: [], &#x27;created_time&#x27;: &#x27;datetime(2016&#x27;, 10: None, &#x27;11)&#x27;: None, &#x27;public_base_image_released_date&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;appstream_agent_version&#x27;: &#x27;string&#x27;, &#x27;image_permissions&#x27;: {}}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>stacks</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `names` and `describe_stacks` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified stacks, if the stack names are provided.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;arn&#x27;: &#x27;string&#x27;, &#x27;name&#x27;: &#x27;string&#x27;, &#x27;description&#x27;: &#x27;string&#x27;, &#x27;display_name&#x27;: &#x27;string&#x27;, &#x27;created_time&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;storage_connectors&#x27;: [], &#x27;redirect_url&#x27;: &#x27;string&#x27;, &#x27;feedback_url&#x27;: &#x27;string&#x27;, &#x27;stack_errors&#x27;: [], &#x27;user_settings&#x27;: [], &#x27;application_settings&#x27;: {}, &#x27;access_endpoints&#x27;: [], &#x27;embed_host_domains&#x27;: []}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>users</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `describe_users` and  `authentication_type` are defined and success</td>
                <td>
                            <div>Retrieves a list that describes one or more specified users in the user pool.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;arn&#x27;: &#x27;string&#x27;, &#x27;user_name&#x27;: &#x27;string&#x27;, &#x27;enabled&#x27;: True, &#x27;status&#x27;: &#x27;string&#x27;, &#x27;first_name&#x27;: &#x27;string&#x27;, &#x27;last_name&#x27;: &#x27;string&#x27;, &#x27;created_time&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;authentication_type&#x27;: &#x27;USERPOOL&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
