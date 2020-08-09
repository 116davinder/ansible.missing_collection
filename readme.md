## Ansible Custom Libs
* newrelic_deployment
* mapr_service

## export ansible library path
export ANSIBLE_LIBRARY=`pwd`

## why required

```
To Support V2 Api of NewRelic for Recording of deployment.
```

* mapr_service
```
To manage mapr services using rest api.
```

### examples
```
- newrelic_deployment:
    token: XXXXXXXXX
    app_name: ansibleApp
    user: ansible deployment user
    revision: '1.X'

- mapr_service:
    username: mapr
    password: mapr
    service_name: nfs
    mcs_url: demo.mapr.com
    mcs_port: 8443
    state: restart
    validate_certs: false
```

