.. _community.missing_collection.aws_backup_info_module:


********************************************
community.missing_collection.aws_backup_info
********************************************

**Get Information about AWS Backup.**


Version added: 1.4.0

.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Get Information about AWS Backup.
- https://docs.aws.amazon.com/aws-backup/latest/devguide/API_Operations.html



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
                    <b>backup_plan_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Id of Backup Plan.</div>
                        <div>Mutually Exclusive with <em>list_backup_plans_include_deleted</em>, <em>list_backup_plan_templates</em>.</div>
                        <div><em>list_backup_vaults</em>, <em>list_backup_jobs</em> and <em>list_copy_jobs</em></div>
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
                    <b>list_backup_jobs</b>
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
                        <div>do you want to fetch backup jobs?</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_jobs_by_account_id</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup jobs by account id used in backup job.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_jobs_by_backup_vault_name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup jobs by backup vault name.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_jobs_by_resource_arn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup jobs by resource arn.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_jobs_by_resource_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup jobs by resource type used in backup job.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_jobs_by_state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup jobs by job state.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_plan_templates</b>
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
                        <div>do you want to fetch backup plan templates?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_plan_versions</b>
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
                        <div>do you want to fetch backup plan versions?</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupPlanVersions.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupPlanVersions.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_plans_include_deleted</b>
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
                        <div>do you want to include deleted backup plans?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_selections</b>
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
                        <div>do you want to fetch backup selections?</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupSelections.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListBackupSelections.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_backup_vaults</b>
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
                        <div>do you want to fetch list of backup vaults?</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs</b>
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
                        <div>do you want to fetch backup copy jobs?</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs_by_account_id</b>
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
                        <div>fetch backup copy jobs by account id.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs_by_destination_vault_arn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup copy jobs by destination vault arn?</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs_by_resource_arn</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup copy jobs by resource arn.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs_by_resource_type</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup copy jobs by resource type.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>list_copy_jobs_by_state</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>fetch backup copy jobs by state of job.</div>
                        <div><a href='https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html'>https://docs.aws.amazon.com/aws-backup/latest/devguide/API_ListCopyJobs.html</a></div>
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

    - name: "get list of aws backup plans without deleted plans"
      aws_backup_info:
      register: __b

    - name: "get list of aws backup plans with deleted plans"
      aws_backup_info:
        list_backup_plans_include_deleted: true

    - name: "get basic details about specific backup plan"
      aws_backup_info:
        backup_plan_id: "{{ __b.backup_plans[0].backup_plan_id }}"
        list_backup_selections: true

    - name: "get list of backup plan versions about specific backup plan"
      aws_backup_info:
        backup_plan_id: "{{ __b.backup_plans[0].backup_plan_id }}"
        list_backup_plan_versions: true

    - name: "get list of backup plan templates"
      aws_backup_info:
        list_backup_plan_templates: true

    - name: "get list of backup vaults"
      aws_backup_info:
        list_backup_vaults: true

    - name: "get list of backup jobs for given backup vault name"
      aws_backup_info:
        list_backup_jobs: true
        list_backup_jobs_by_backup_vault_name: 'rds-valut'

    - name: "list of backup jobs for given vault name and state"
      aws_backup_info:
        list_backup_jobs: true
        list_backup_jobs_by_backup_vault_name: 'rds-valut'
        list_backup_jobs_by_state: 'COMPLETED'

    - name: "list of backup copy jobs"
      aws_backup_info:
        list_copy_jobs: true
        list_copy_jobs_by_state: 'COMPLETED'



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
                    <b>backup_jobs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `list_backup_jobs` and any filter values are passed like `list_backup_jobs_by_backup_vault_name`, `list_backup_jobs_by_state` `list_backup_jobs_by_resource_arn`, `list_backup_jobs_by_resource_type` `list_backup_jobs_by_account_id` and success</td>
                <td>
                            <div>List of backup jobs.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;account_id&#x27;: &#x27;xxxx&#x27;, &#x27;backup_job_id&#x27;: &#x27;9AA49310-xxxx-6B3522195FDB&#x27;, &#x27;backup_size_in_bytes&#x27;: 0, &#x27;backup_vault_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxx:backup-vault:rds-valut&#x27;, &#x27;backup_vault_name&#x27;: &#x27;rds-valut&#x27;, &#x27;completion_date&#x27;: &#x27;2020-12-23T01:28:05.634000+02:00&#x27;, &#x27;created_by&#x27;: {&#x27;backup_plan_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_id&#x27;: &#x27;55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_version&#x27;: &#x27;ODJhZDFhOWIxxxxxxxYjA5ZGYyZDgx&#x27;, &#x27;backup_rule_id&#x27;: &#x27;8430c4d0-xxxxxxxxx-54c449719284&#x27;}, &#x27;creation_date&#x27;: &#x27;2020-12-23T01:14:33.406000+02:00&#x27;, &#x27;iam_role_arn&#x27;: &#x27;arn:aws:iam::xxxxxx:role/service-role/AWSBackupDefaultServiceRole&#x27;, &#x27;percent_done&#x27;: &#x27;100.0&#x27;, &#x27;recovery_point_arn&#x27;: &#x27;arn:aws:rds:us-east-1:xxxxxxx:snapshot:awsbackup:job-9aa49310-xxxxx-6b3522195fdb&#x27;, &#x27;resource_arn&#x27;: &#x27;arn:aws:rds:us-east-1:xxxxxxxxxxx:db:test&#x27;, &#x27;resource_type&#x27;: &#x27;RDS&#x27;, &#x27;start_by&#x27;: &#x27;2020-12-23T02:10:00+02:00&#x27;, &#x27;state&#x27;: &#x27;COMPLETED&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_plan_selections</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `backup_plan_id`, `list_backup_selections` and success</td>
                <td>
                            <div>List of backup plans selections.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;backup_plan_id&#x27;: &#x27;55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;creation_date&#x27;: &#x27;2020-11-16T14:33:42.554000+02:00&#x27;, &#x27;creator_request_id&#x27;: &#x27;8dd55ad7-xxx-47edc804e3d3&#x27;, &#x27;iam_role_arn&#x27;: &#x27;arn:aws:iam::xxxxx:role/service-role/AWSBackupDefaultServiceRole&#x27;, &#x27;selection_id&#x27;: &#x27;06c9f85f-c49e-4efb-ace3-b1fd1ef86862&#x27;, &#x27;selection_name&#x27;: &#x27;test-rds&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_plan_templates</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `list_backup_plan_templates` and success</td>
                <td>
                            <div>List of backup plans templates.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;backup_plan_template_id&#x27;: &#x27;87c0c1ef-xxxxxx-2e76a2c38aaa&#x27;, &#x27;backup_plan_template_name&#x27;: &#x27;Daily-35day-Retention&#x27;}, {&#x27;backup_plan_template_id&#x27;: &#x27;87c0c1ef-xxxxxx-2e76a2c38aab&#x27;, &#x27;backup_plan_template_name&#x27;: &#x27;Daily-Monthly-1yr-Retention&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_plan_versions</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `backup_plan_id`, `list_backup_plan_versions` and success</td>
                <td>
                            <div>List of backup plans versions.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;backup_plan_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxxx:backup-plan:55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_id&#x27;: &#x27;55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_name&#x27;: &#x27;test-rds-backup&#x27;, &#x27;creation_date&#x27;: &#x27;2020-11-16T16:08:15.039000+02:00&#x27;, &#x27;last_execution_date&#x27;: &#x27;2020-12-23T01:14:33.406000+02:00&#x27;, &#x27;version_id&#x27;: &#x27;ODJhZDFhOWItYxxxxxxxYjA5ZGYyZDgx&#x27;}, {&#x27;backup_plan_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_id&#x27;: &#x27;55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_name&#x27;: &#x27;test-rds-backup&#x27;, &#x27;creation_date&#x27;: &#x27;2020-11-16T14:55:46.131000+02:00&#x27;, &#x27;deletion_date&#x27;: &#x27;2020-11-16T16:08:15.039000+02:00&#x27;, &#x27;last_execution_date&#x27;: &#x27;2020-11-16T16:07:47.272000+02:00&#x27;, &#x27;version_id&#x27;: &#x27;ZDliN2U5YjMxxxxxI1NmU4Y2U1MDk5&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_plans</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when no argument is defined or `list_backup_plans_include_deleted` and success</td>
                <td>
                            <div>List of backup plans.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;backup_plan_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxx:backup-plan:55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_id&#x27;: &#x27;55934731-xxxxx-a4a44b98f40b&#x27;, &#x27;backup_plan_name&#x27;: &#x27;test-rds-backup&#x27;, &#x27;creation_date&#x27;: &#x27;2020-11-16T16:08:15.039000+02:00&#x27;, &#x27;last_execution_date&#x27;: &#x27;2020-12-23T01:14:33.406000+02:00&#x27;, &#x27;version_id&#x27;: &#x27;ODJhZDFhxxxxxxxxxA5ZGYyZDgx&#x27;}, {&#x27;backup_plan_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxxx:backup-plan:74a37778-xxxxx-9176d22ae8f2&#x27;, &#x27;backup_plan_id&#x27;: &#x27;74a37778-xxxxx-9176d22ae8f2&#x27;, &#x27;backup_plan_name&#x27;: &#x27;Test&#x27;, &#x27;creation_date&#x27;: &#x27;2020-10-13T15:39:45.605000+03:00&#x27;, &#x27;deletion_date&#x27;: &#x27;2020-10-13T16:58:10.741000+03:00&#x27;, &#x27;last_execution_date&#x27;: &#x27;2020-10-13T16:33:12.037000+03:00&#x27;, &#x27;version_id&#x27;: &#x27;Yzk2YWJmMTxxxxxFkNTNmNTRm&#x27;}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>backup_vaults</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `list_backup_vaults` and success</td>
                <td>
                            <div>List of backup vaults.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;backup_vault_arn&#x27;: &#x27;arn:aws:backup:us-east-1:xxxx:backup-vault:Default&#x27;, &#x27;backup_vault_name&#x27;: &#x27;Default&#x27;, &#x27;creation_date&#x27;: &#x27;2019-01-28T10:31:25.594000+02:00&#x27;, &#x27;creator_request_id&#x27;: &#x27;Default&#x27;, &#x27;encryption_key_arn&#x27;: &#x27;arn:aws:kms:us-east-1:xxxx:key/8308c521-xxxxx-86bda5017bf4&#x27;, &#x27;number_of_recovery_points&#x27;: 0}]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>copy_jobs</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>when `list_copy_jobs` and any filter values are passed like `list_copy_jobs_by_state`, `list_copy_jobs_by_resource_arn`, `list_copy_jobs_by_resource_type`, `list_copy_jobs_by_account_id` `list_copy_jobs_by_destination_vault_arn` and success</td>
                <td>
                            <div>List of backup copy jobs.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[{&#x27;account_id&#x27;: &#x27;string&#x27;, &#x27;copy_job_id&#x27;: &#x27;string&#x27;, &#x27;source_backup_vault_arn&#x27;: &#x27;string&#x27;, &#x27;source_recovery_point_arn&#x27;: &#x27;string&#x27;, &#x27;destination_backup_vault_arn&#x27;: &#x27;string&#x27;, &#x27;destination_recovery_point_arn&#x27;: &#x27;string&#x27;, &#x27;resource_arn&#x27;: &#x27;string&#x27;, &#x27;creation_date&#x27;: &#x27;datetime(2015&#x27;, 1: None, &#x27;1)&#x27;: None, &#x27;completion_date&#x27;: &#x27;datetime(2015&#x27;, &#x27;state&#x27;: &#x27;CREATED&#x27;, &#x27;status_message&#x27;: &#x27;string&#x27;, &#x27;backup_size_in_bytes&#x27;: 123, &#x27;iam_role_arn&#x27;: &#x27;string&#x27;, &#x27;created_by&#x27;: {&#x27;backup_plan_id&#x27;: &#x27;string&#x27;, &#x27;backup_plan_arn&#x27;: &#x27;string&#x27;, &#x27;backup_plan_version&#x27;: &#x27;string&#x27;, &#x27;backup_rule_id&#x27;: &#x27;string&#x27;}, &#x27;resource_type&#x27;: &#x27;string&#x27;}]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Davinder Pal (@116davinder) <dpsangwal@gmail.com>
