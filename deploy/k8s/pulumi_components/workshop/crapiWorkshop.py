import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWorkshop(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWorkshop", name, {}, opts)

        crapi_workshop = kubernetes.apps.v1.Deployment(f"{name}-crapiWorkshop",
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
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
