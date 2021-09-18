#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Davinder Pal <dpsangwal@gmail.com>

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = """
module: doh
short_description: DNS Lookup over HTTPS.
description:
  - DNS Lookup over HTTPS from various Public DOH Servers like Google/Cloudflare/Quad9.
  - U(https://developers.cloudflare.com/1.1.1.1/encrypted-dns/dns-over-https/make-api-requests/dns-json)
  - U(https://developers.google.com/speed/public-dns/docs/doh/json)
  - U(https://www.quad9.net/news/blog/doh-with-quad9-dns-servers/)
version_added: 0.4.0
options:
  source:
    description:
      - DNS over HTTPS can be queried from Google/Cloudflare/Quad9.
    required: false
    type: str
    choices: ["google", "cloudflare", "quad9"]
    default: "cloudflare"
  domain_name:
    description:
      - domain name or hostname for lookup.
    required: true
    type: str
  type:
    description:
      - type of dns lookup.
    required: false
    type: str
    default: "A"
  do:
    description:
      - set if client wants DNSSEC data.
    required: false
    type: bool
    default: true
  cd:
    description:
      - set to disable validation.
    required: false
    type: bool
    default: false
author:
  - "Davinder Pal (@116davinder) <dpsangwal@gmail.com>"
requirements:
  - requests
"""

EXAMPLES = """
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
"""

RETURN = """
result:
  description: result of the api request.
  returned: when success.
  type: dict
  sample: {
    "Status": 0,
    "TC": false,
    "RD": true,
    "RA": true,
    "AD": true,
    "CD": false,
    "Question": [
      {
        "name": "example.com.",
        "type": 28
      }
    ],
    "Answer": [
      {
        "name": "example.com.",
        "type": 28,
        "TTL": 1726,
        "data": "2606:2800:220:1:248:1893:25c8:1946"
      }
    ]
  }
"""

from ansible.module_utils.basic import AnsibleModule
import requests


def main():
    argument_spec = dict(
        source=dict(choices=["google", "cloudflare", "quad9"], default="cloudflare"),
        domain_name=dict(required=True, aliases=["name"]),
        type=dict(default="A"),
        do=dict(type=bool, default=True),
        cd=dict(type=bool, default=False),
    )

    module = AnsibleModule(
        argument_spec=argument_spec,
    )

    headers = {
        "accept": "application/dns-json"
    }
    params = {
        "name": module.params["domain_name"],
        "type": module.params["type"],
        "do": module.params["do"],
        "cd": module.params["cd"]
    }

    dns_urls = {
        "cloudflare": "https://cloudflare-dns.com/dns-query",
        "google": "https://dns.google/resolve",
        "quad9": "https://dns.quad9.net:5053/dns-query",
    }

    if module.params["source"] in dns_urls.keys():
        r = requests.get(
            url=dns_urls[module.params["source"]],
            params=params,
            headers=headers
        )
    else:
        module.fail_json("unknown options are passed")

    if r.status_code == 200:
        module.exit_json(changed=True, result=r.json())
    else:
        module.fail_json(msg=r.text)


if __name__ == "__main__":
    main()
