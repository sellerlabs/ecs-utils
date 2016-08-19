# ECS Utils

## Deploy Workflow

`deploy.py <app-definition> <app env> <tag>`

`deploy.py foo-app.json stage v0.1.0`

`foo-app.json`
```json
{"envs": {"prod": {"cluster": "prod-cluster-id",
                   "tasks": {"migrate": {"template": "migrate.json",
                                         "family": "migrate-prod-task-id",
                                         "containerName": "migrate-prod-container-id"}},
                    "services": {"http": {"id": "http-prod-service-id",
                                          "family": "http-prod-task-id",
                                          "containerName": "http-prod-container-id",
                                          "template": "http-prod.json"},
                                 "worker": {"id": "worker-prod-service-id",
                                            "family": "worker-prod-task-id",
                                            "containerName": "worker-prod-container-id",
                                            "template": "worker-prod.json"}}},
          "stage": {"cluster": "stage cluster id",
                    "tasks": {"migrate": {"template": "migrate.json",
                                          "family": "migrate-stage-task-id",
                                          "containerName": "migrate-stage-container-id"}},
                    "services": {"http": {"id": "http-stage-service-id",
                                          "family": "http-stage-task-id",
                                          "containerName": "http-stage-container-id",
                                          "template": "http-stage.json"},
                                 "worker": {"id": "worker-stage-service-id",
                                            "family": "worker-stage-task-id",
                                            "containerName": "worker-stage-container-id",
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
