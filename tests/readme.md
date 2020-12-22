## Testing locally

**Note**

No need to use full collection name in test playbook code.

* update the code in `plugins/modules/<module>.py`
* export ANSIBLE_LIBRARY=`<clone repository path>/plugins/modules`
* create/update test playbook in `tests/<module>.yml`