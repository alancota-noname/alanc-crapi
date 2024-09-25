import pulumi
import pulumi_kubernetes as kubernetes

crapi_web = kubernetes.apps.v1.Deployment("crapiWeb",
    metadata={
        "name": "crapi-web",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "crapi-web",
            },
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "crapi-web",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "crapi-web-configmap",
                        },
                    }],
                    "image": "crapi/crapi-web:latest",
                    "image_pull_policy": "Always",
                    "name": "crapi-web",
                    "ports": [{
                        "container_port": 80,
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
            },
        },
    })
crapi_web1 = kubernetes.core.v1.Service("crapiWeb1",
    metadata={
        "labels": {
            "app": "crapi-web",
        },
        "name": "crapi-web",
    },
    spec={
        "ports": [{
            "name": "nginx",
            "node_port": 30080,
            "port": 80,
        }],
        "selector": {
            "app": "crapi-web",
        },
        "type": kubernetes.core.v1.ServiceSpecType.LOAD_BALANCER,
    })
crapi_web_configmap = kubernetes.core.v1.ConfigMap("crapiWebConfigmap",
    data={
        "COMMUNITY_SERVICE": "crapi-community:8087",
        "IDENTITY_SERVICE": "crapi-identity:8080",
        "WORKSHOP_SERVICE": "crapi-workshop:8000",
    },
    metadata={
        "labels": {
            "app": "crapi-web",
        },
        "name": "crapi-web-configmap",
    })
