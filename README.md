# ECS Utils

## Deploy Workflow

`deploy.py <app-definition> <app env> <tag>`

`deploy.py foo-app.json stage v0.1.0`

`foo-app.json`
```json
{"envs": {"prod": {"cluster": "prod-cluster-id",
                    "services": {"http": {"id": "http-prod-service-id",
                                          "template": "http-prod.json"},
                                 "worker": {"id": "worker-prod-service-id",
                                            "template": "worker-prod.json"}}},
          "stage": {"cluster": "stage cluster id",
                    "services": {"http": {"id": "http-stage-service-id",
                                          "template": "http-stage.json"},
                                 "worker": {"id": "worker-stage-service-id",
                                            "template": "worker-stage.json"}}}},
 "image": "image-host/path"}
```

`http-prod-service.json`

```json
{
    "family": <ecs-family>,
    "volumes": [],
    "containerDefinitions": [
        {
            "environment": [],
            "name": "foo-app",
            "links": [],
            "mountPoints": [],
            "image": "",
            "logConfiguration": {
                "logDriver": "syslog"
            },
            "essential": true,
            "portMappings": [
                {
                    "protocol": "tcp",
                    "containerPort": 8080,
                    "hostPort": 80
                }
            ],
            "entryPoint": [],
            "memory": 3800,
            "command": [
                "lein",
                "trampoline",
                "http"
            ],
            "cpu": 1,
            "volumesFrom": []
        }
    ]
}
```
