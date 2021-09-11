#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: capabilities_info
short_description: Get information about linux capability of given file.
description:
  - Get information about linux capability of given file.
  - U(https://reposcope.com/package/libcap)
  - It requires B(libcap) package.
version_added: 0.3.0
options:
  path:
    description:
      - path of the file.
    required: true
    type: str
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
"""

EXAMPLES = """
- name: get all linux capabilities for ping binary
  community.missing_collection.capabilities_info:
    path: '/usr/bin/ping'
"""

RETURN = """
capabilities:
  description: list of the linux capabilites.
  returned: when success.
  type: list
  sample: ["cap_net_bind_service", "cap_net_admin=ep"]
"""

from ansible.module_utils.basic import AnsibleModule
import os
import ctypes
import ctypes.util


def main():
    argument_spec = dict(
        path=dict(required=True),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    # find libcap library in the system
    _cap_lib = ctypes.util.find_library('cap')

    if _cap_lib:
        _libcap = ctypes.cdll.LoadLibrary(_cap_lib)
        _libcap.cap_to_text.restype = ctypes.c_char_p
    else:
        module.fail_json("please install libcap package which provides libcap.so")

    _path = module.params["path"]

    if os.path.exists(_path):
        caps = _libcap.cap_get_file(_path.encode("utf-8"))
        caps_text = _libcap.cap_to_text(caps, None)
        if caps_text:
            module.exit_json(capabilities=caps_text.decode("utf-8").split(","))
        else:
            module.exit_json(capabilities=list())
    else:
        module.fail_json("{} path not found".format(_path))


if __name__ == "__main__":
    main()
