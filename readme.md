## Ansible Custom Libs
* newrelic_deployment

## why required
* newrelic_deployment
```
To Support V2 Api of NewRelic for Recording of deployment.
```

### example
```
- newrelic_deployment:
    token: XXXXXXXXX
    app_name: ansibleApp
    user: ansible deployment user
    revision: '1.X'
```

