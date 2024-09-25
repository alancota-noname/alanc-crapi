import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiCommunity(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiCommunity", name, {}, opts)

        crapi_community = kubernetes.apps.v1.Deployment(f"{name}-crapiCommunity",
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
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
