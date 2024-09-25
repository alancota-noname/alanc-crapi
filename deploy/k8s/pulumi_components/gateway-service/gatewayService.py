import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class GatewayService(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:GatewayService", name, {}, opts)

        gateway_service = kubernetes.apps.v1.Deployment(f"{name}-gatewayService",
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
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
