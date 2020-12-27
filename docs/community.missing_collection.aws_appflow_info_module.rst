.. _community.missing_collection.aws_appflow_info_module:


*********************************************
community.missing_collection.aws_appflow_info
*********************************************

**Get details about AWS AppFlow Service.**


Version added: 0.0.2

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get Information about AWS AppFlow Service.
- https://docs.aws.amazon.com/appflow/1.0/APIReference/API_Operations.html



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
                    <b>describe_connector_types</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>list of type of appflow connectors.</div>
                        <div><a href='https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html'>https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_connectors</b>
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
                        <div>do you want to describe aws appflow connector for given list of <em>describe_connector_types</em>.</div>
                        <div><a href='https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html'>https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeConnectors.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>describe_flow</b>
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
                        <div>do you want to describe aws appflow for given <em>name</em>.</div>
                        <div><a href='https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeFlow.html'>https://docs.aws.amazon.com/appflow/1.0/APIReference/API_DescribeFlow.html</a></div>
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
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>name of aws appflow.</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: flow_name</div>
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

    - name: "list aws app flows"
      aws_appflow_info:

    - name: "describe aws app flow name"
      aws_appflow_info:
        name: 'test'
        describe_flow: true

    - name: "describe aws app flow connector"
      aws_appflow_info:
        describe_connectors: true
        describe_connector_types: ['S3']



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
                    <b>connector_configurations</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when `describe_connectors` and `describe_connector_types` are defined and success</td>
                <td>
                            <div>Information about given appflow connector configurations.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;s3&#x27;: {&#x27;can_use_as_destination&#x27;: True, &#x27;can_use_as_source&#x27;: True, &#x27;connector_metadata&#x27;: {&#x27;s3&#x27;: {}}, &#x27;is_private_link_enabled&#x27;: False, &#x27;is_private_link_endpoint_url_required&#x27;: False, &#x27;supported_destination_connectors&#x27;: [&#x27;Salesforce&#x27;, &#x27;Snowflake&#x27;, &#x27;Redshift&#x27;, &#x27;S3&#x27;], &#x27;supported_scheduling_frequencies&#x27;: [&#x27;BYMINUTE&#x27;, &#x27;HOURLY&#x27;, &#x27;DAILY&#x27;, &#x27;WEEKLY&#x27;, &#x27;MONTHLY&#x27;, &#x27;ONCE&#x27;], &#x27;supported_trigger_types&#x27;: [&#x27;Scheduled&#x27;, &#x27;OnDemand&#x27;]}}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>flow</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when `flow_name` is defined and `describe_flow=true` and success</td>
                <td>
                            <div>Information about given flow name.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;created_at&#x27;: &#x27;2020-12-26T18:52:43.076000+02:00&#x27;, &#x27;created_by&#x27;: &#x27;arn:aws:iam::xxxxxxxxxxx:user/xxxxxxxxxxxx&#x27;, &#x27;description&#x27;: &#x27;test flow&#x27;, &#x27;destination_flow_config_list&#x27;: [{&#x27;connector_type&#x27;: &#x27;S3&#x27;, &#x27;destination_connector_properties&#x27;: {&#x27;s3&#x27;: {&#x27;bucket_name&#x27;: &#x27;test-bucket-s3&#x27;, &#x27;s3_output_format_config&#x27;: {&#x27;aggregation_config&#x27;: {&#x27;aggregation_type&#x27;: &#x27;None&#x27;}, &#x27;file_type&#x27;: &#x27;JSON&#x27;, &#x27;prefix_config&#x27;: {}}}}}], &#x27;flow_arn&#x27;: &#x27;arn:aws:appflow:us-east-1:xxxxxxxxxxxx:flow/test&#x27;, &#x27;flow_name&#x27;: &#x27;test&#x27;, &#x27;flow_status&#x27;: &#x27;Active&#x27;, &#x27;kms_arn&#x27;: &#x27;arn:aws:kms:us-east-1:xxxxxxxxxxx:key/xxxxxxxxxxx-a32c-59fe2257d2b4&#x27;, &#x27;last_updated_at&#x27;: &#x27;2020-12-26T18:52:43.076000+02:00&#x27;, &#x27;last_updated_by&#x27;: &#x27;arn:aws:iam::xxxxxxxxxxx:user/xxxxxxxxxxx&#x27;, &#x27;response_metadata&#x27;: {&#x27;http_headers&#x27;: {&#x27;connection&#x27;: &#x27;keep-alive&#x27;, &#x27;content-length&#x27;: &#x27;3157&#x27;, &#x27;content-type&#x27;: &#x27;application/json&#x27;, &#x27;date&#x27;: &#x27;Sat, 26 Dec 2020 16:55:16 GMT&#x27;, &#x27;x-amz-apigw-id&#x27;: &#x27;YK2xxxxxxxxxxxxxxFVMw=&#x27;, &#x27;x-amzn-requestid&#x27;: &#x27;xxxxxxxxxxxxx-86f9-ceb6cfe1ce41&#x27;, &#x27;x-amzn-trace-id&#x27;: &#x27;Root=1-xxxxxxxxxxxxxxxd30a371c2a38&#x27;}, &#x27;http_status_code&#x27;: 200, &#x27;request_id&#x27;: &#x27;769ebe3d-4407-45a4-86f9-ceb6cfe1ce41&#x27;, &#x27;retry_attempts&#x27;: 0}, &#x27;source_flow_config&#x27;: {&#x27;connector_type&#x27;: &#x27;S3&#x27;, &#x27;source_connector_properties&#x27;: {&#x27;s3&#x27;: {&#x27;bucket_name&#x27;: &#x27;test-s3-bucket&#x27;, &#x27;bucket_prefix&#x27;: &#x27;sample&#x27;}}}, &#x27;tags&#x27;: {}, &#x27;tasks&#x27;: [{&#x27;connector_operator&#x27;: {&#x27;s3&#x27;: &#x27;PROJECTION&#x27;}, &#x27;source_fields&#x27;: [&#x27;{  &#x27;], &#x27;task_properties&#x27;: {}, &#x27;task_type&#x27;: &#x27;Filter&#x27;}, {&#x27;connector_operator&#x27;: {&#x27;s3&#x27;: &#x27;NO_OP&#x27;}, &#x27;destination_field&#x27;: &#x27;{  &#x27;, &#x27;source_fields&#x27;: [&#x27;{  &#x27;], &#x27;task_properties&#x27;: {}, &#x27;task_type&#x27;: &#x27;Map&#x27;}], &#x27;trigger_config&#x27;: {&#x27;trigger_properties&#x27;: {}, &#x27;trigger_type&#x27;: &#x27;OnDemand&#x27;}}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>flows</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when no arguments and success</td>
                <td>
                            <div>List of aws appflows.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;created_at&#x27;: &#x27;2020-12-26T18:52:43.076000+02:00&#x27;, &#x27;created_by&#x27;: &#x27;arn:aws:iam::xxxx:user/xxxx&#x27;, &#x27;description&#x27;: &#x27;test flow&#x27;, &#x27;destination_connector_type&#x27;: &#x27;S3&#x27;, &#x27;flow_arn&#x27;: &#x27;arn:aws:appflow:us-east-1:xxxxxxxx:flow/test&#x27;, &#x27;flow_name&#x27;: &#x27;test&#x27;, &#x27;flow_status&#x27;: &#x27;Active&#x27;, &#x27;last_updated_at&#x27;: &#x27;2020-12-26T18:52:43.076000+02:00&#x27;, &#x27;last_updated_by&#x27;: &#x27;arn:aws:iam::xxxxxxxxxx:user/xxxxx&#x27;, &#x27;source_connector_type&#x27;: &#x27;S3&#x27;, &#x27;tags&#x27;: {}, &#x27;trigger_type&#x27;: &#x27;OnDemand&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
