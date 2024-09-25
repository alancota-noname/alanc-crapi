import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiIdentity(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiIdentity", name, {}, opts)

        crapi_identity = kubernetes.apps.v1.Deployment(f"{name}-crapiIdentity",
            metadata={
                "name": "crapi-identity",
            },
            spec={
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": "crapi-identity",
                    },
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "crapi-identity",
                        },
                    },
                    "spec": {
                        "containers": [{
                            "env_from": [{
                                "config_map_ref": {
                                    "name": "crapi-identity-configmap",
                                },
                            }],
                            "image": "crapi/crapi-identity:latest",
                            "image_pull_policy": "Always",
                            "name": "crapi-identity",
                            "ports": [{
                                "container_port": 8080,
                            }],
                            "readiness_probe": {
                                "initial_delay_seconds": 15,
                                "period_seconds": 10,
                                "tcp_socket": {
                                    "port": 8080,
                                },
                            },
                            "resources": {
                                "limits": {
                                    "cpu": "500m",
                                },
                                "requests": {
                                    "cpu": "256m",
                                },
                            },
                            "volume_mounts": [{
                                "mount_path": "/.keys",
                                "name": "jwt-key-secret",
                                "read_only": True,
                            }],
                        }],
                        "init_containers": [{
                            "args": [
                                "service",
                                "postgresdb",
                            ],
                            "image": "groundnuty/k8s-wait-for:v1.3",
                            "image_pull_policy": "Always",
                            "name": "wait-for-postgres",
                        }],
                        "volumes": [{
                            "name": "jwt-key-secret",
                            "secret": {
                                "secret_name": "jwt-key-secret",
                            },
                        }],
                    },
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
