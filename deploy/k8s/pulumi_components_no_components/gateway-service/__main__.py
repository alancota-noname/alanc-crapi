import pulumi
import pulumi_kubernetes as kubernetes

gateway_service = kubernetes.apps.v1.Deployment("gatewayService",
    metadata={
        "name": "gateway-service",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "gateway-service",
            },
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "gateway-service",
                },
            },
            "spec": {
                "containers": [{
                    "image": "crapi/gateway-service:latest",
                    "image_pull_policy": "Always",
                    "name": "gateway-service",
                    "ports": [{
                        "container_port": 8087,
                    }],
                    "resources": {
                        "limits": {
                            "cpu": "100m",
                        },
                        "requests": {
                            "cpu": "50m",
                        },
                    },
                }],
            },
        },
    })
gateway_service_configmap = kubernetes.core.v1.ConfigMap("gatewayServiceConfigmap",
    data={
        "SERVER_PORT": "443",
    },
    metadata={
        "labels": {
            "app": "gateway-service",
        },
        "name": "gateway-service-configmap",
    })
gateway_service1 = kubernetes.core.v1.Service("gatewayService1",
    metadata={
        "labels": {
            "app": "gateway-service",
        },
        "name": "gateway-service",
    },
    spec={
        "ports": [{
            "name": "go",
            "port": 8087,
        }],
        "selector": {
            "app": "gateway-service",
        },
    })
