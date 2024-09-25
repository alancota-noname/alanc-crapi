import pulumi
import pulumi_kubernetes as kubernetes

crapi_workshop = kubernetes.apps.v1.Deployment("crapiWorkshop",
    metadata={
        "name": "crapi-workshop",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "crapi-workshop",
            },
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "crapi-workshop",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "crapi-workshop-configmap",
                        },
                    }],
                    "image": "crapi/crapi-workshop:latest",
                    "image_pull_policy": "Always",
                    "name": "crapi-workshop",
                    "ports": [{
                        "container_port": 8000,
                    }],
                    "readiness_probe": {
                        "initial_delay_seconds": 15,
                        "period_seconds": 10,
                        "tcp_socket": {
                            "port": 8000,
                        },
                    },
                    "resources": {
                        "limits": {
                            "cpu": "256m",
                        },
                        "requests": {
                            "cpu": "256m",
                        },
                    },
                }],
                "init_containers": [
                    {
                        "args": [
                            "service",
                            "crapi-identity",
                        ],
                        "image": "groundnuty/k8s-wait-for:v1.3",
                        "image_pull_policy": "Always",
                        "name": "wait-for-crapi-identity",
                    },
                    {
                        "args": [
                            "service",
                            "crapi-community",
                        ],
                        "image": "groundnuty/k8s-wait-for:v1.3",
                        "image_pull_policy": "Always",
                        "name": "wait-for-crapi-community",
                    },
                ],
            },
        },
    })
crapi_workshop_configmap = kubernetes.core.v1.ConfigMap("crapiWorkshopConfigmap",
    data={
        "DB_DRIVER": "postgres",
        "DB_HOST": "postgresdb",
        "DB_NAME": "crapi",
        "DB_PASSWORD": "crapisecretpassword",
        "DB_PORT": "5432",
        "DB_USER": "admin",
        "IDENTITY_SERVICE": "crapi-identity:8080",
        "MONGO_DB_DRIVER": "mongodb",
        "MONGO_DB_HOST": "mongodb",
        "MONGO_DB_NAME": "crapi",
        "MONGO_DB_PASSWORD": "crapisecretpassword",
        "MONGO_DB_PORT": "27017",
        "MONGO_DB_USER": "admin",
        "SECRET_KEY": "crapi",
        "SERVER_PORT": "8000",
    },
    metadata={
        "labels": {
            "app": "crapi-workshop",
        },
        "name": "crapi-workshop-configmap",
    })
crapi_workshop1 = kubernetes.core.v1.Service("crapiWorkshop1",
    metadata={
        "labels": {
            "app": "crapi-workshop",
        },
        "name": "crapi-workshop",
    },
    spec={
        "ports": [{
            "name": "python",
            "port": 8000,
        }],
        "selector": {
            "app": "crapi-workshop",
        },
    })
