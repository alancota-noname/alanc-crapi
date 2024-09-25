import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Mailhog(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Mailhog", name, {}, opts)

        mailhog = kubernetes.apps.v1.Deployment(f"{name}-mailhog",
            metadata={
                "name": "mailhog",
                "namespace": "crapi",
            },
            spec={
                "min_ready_seconds": 10,
                "progress_deadline_seconds": 600,
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": "mailhog",
                    },
                },
                "template": {
                    "metadata": {
                        "annotations": {
                            "sidecar_traceable_ai_inject": "false",
                        },
                        "labels": {
                            "app": "mailhog",
                        },
                    },
                    "spec": {
                        "containers": [{
                            "env_from": [{
                                "config_map_ref": {
                                    "name": "mailhog-configmap",
                                },
                            }],
                            "image": "crapi/mailhog:latest",
                            "image_pull_policy": "Always",
                            "liveness_probe": {
                                "initial_delay_seconds": 15,
                                "period_seconds": 60,
                                "tcp_socket": {
                                    "port": 1025,
                                },
                            },
                            "name": "mailhog",
                            "ports": [
                                {
                                    "container_port": 8025,
                                    "name": "web",
                                    "protocol": "TCP",
                                },
                                {
                                    "container_port": 1025,
                                    "name": "smtp",
                                    "protocol": "TCP",
                                },
                            ],
                            "readiness_probe": {
                                "initial_delay_seconds": 15,
                                "period_seconds": 20,
                                "tcp_socket": {
                                    "port": 1025,
                                },
                            },
                            "resources": {
                                "limits": {
                                    "cpu": "1",
                                    "memory": "1024Mi",
                                },
                                "requests": {
                                    "cpu": "50m",
                                    "memory": "64Mi",
                                },
                            },
                        }],
                        "security_context": {
                            "run_as_group": 0,
                            "run_as_user": 0,
                        },
                    },
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
