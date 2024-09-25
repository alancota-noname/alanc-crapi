import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWeb(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWeb", name, {}, opts)

        crapi_web = kubernetes.apps.v1.Deployment(f"{name}-crapiWeb",
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
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
