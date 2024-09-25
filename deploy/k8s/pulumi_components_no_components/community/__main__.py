import pulumi
import pulumi_kubernetes as kubernetes

crapi_community = kubernetes.apps.v1.Deployment("crapiCommunity",
    metadata={
        "name": "crapi-community",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "crapi-community",
            },
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "crapi-community",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "crapi-community-configmap",
                        },
                    }],
                    "image": "crapi/crapi-community:latest",
                    "image_pull_policy": "Always",
                    "name": "crapi-community",
                    "ports": [{
                        "container_port": 8087,
                    }],
                    "resources": {
                        "limits": {
                            "cpu": "500m",
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
                            "postgresdb",
                        ],
                        "image": "groundnuty/k8s-wait-for:v1.3",
                        "image_pull_policy": "Always",
                        "name": "wait-for-postgres",
                    },
                    {
                        "args": [
                            "service",
                            "mongodb",
                        ],
                        "image": "groundnuty/k8s-wait-for:v1.3",
                        "image_pull_policy": "Always",
                        "name": "wait-for-mongo",
                    },
                    {
                        "args": [
                            "service",
                            "crapi-identity",
                        ],
                        "image": "groundnuty/k8s-wait-for:v1.3",
                        "image_pull_policy": "Always",
                        "name": "wait-for-java",
                    },
                ],
            },
        },
    })
crapi_community_configmap = kubernetes.core.v1.ConfigMap("crapiCommunityConfigmap",
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
        "SERVER_PORT": "8087",
    },
    metadata={
        "labels": {
            "app": "crapi-community",
        },
        "name": "crapi-community-configmap",
    })
crapi_community1 = kubernetes.core.v1.Service("crapiCommunity1",
    metadata={
        "labels": {
            "app": "crapi-community",
        },
        "name": "crapi-community",
    },
    spec={
        "ports": [{
            "name": "go",
            "port": 8087,
        }],
        "selector": {
            "app": "crapi-community",
        },
    })
