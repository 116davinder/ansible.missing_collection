## Generate Automatic Docs for this collection
### Install ansible automatic doc creation tool ?
```bash
$ pip3 install git+https://github.com/ansible-network/collection_prep.git
```
### #myWay
```bash
bash easy_dev.sh
```

### Manually generate docs from ansible tool ?
```bash
$ collection_prep_add_docs -p . -b master
INFO      Setting collection name to community.missing_collection
INFO      Setting GitHub repository url to https://github.com/116davinder/ansible.missing_collection
INFO      Purging content from directory /home/dpal/python-projects/ansible.missing_collection/docs
INFO      Making docs directory /home/dpal/python-projects/ansible.missing_collection/docs
INFO      Process content in /home/dpal/python-projects/ansible.missing_collection/plugins/modules
INFO      Processing /home/dpal/python-projects/ansible.missing_collection/plugins/modules/aws_amp_info.py
..............
INFO      Processing /tmp/ansible.missing_collection/plugins/modules/aws_machinelearning_info.py
INFO      Processing /tmp/ansible.missing_collection/plugins/modules/aws_appflow_info.py
INFO      Processing /tmp/ansible.missing_collection/plugins/modules/aws_lightsail_info.py
INFO      Processing 'modules' for README
INFO      README.md updated
INFO      README.md updated with ansible compatibility information
```