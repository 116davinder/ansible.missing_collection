# Testing Modules locally

## Notes*

No need to use full collection name in test playbook code.

* install this collection so its helper / `module_utils` functions can be used.

`ansible-galaxy collection install git+https://github.com/116davinder/ansible.missing_collection.git --force`

* update the code in `plugins/modules/<module>.py`

* export ANSIBLE_LIBRARY=`<cloned repository path>/plugins/modules`

* create/update test playbook in `tests/integration/<cloud-provider>/<module>.yml`
