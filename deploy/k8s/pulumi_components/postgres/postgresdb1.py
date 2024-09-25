import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Postgresdb1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Postgresdb1", name, {}, opts)

        postgresdb1 = kubernetes.apps.v1.StatefulSet(f"{name}-postgresdb1",
            metadata={
                "name": "postgresdb",
            },
            spec={
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": "postgresdb",
                    },
                },
                "service_name": "postgresdb",
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "postgresdb",
                        },
                    },
                    "spec": {
                        "containers": [{
                            "args": [
                                "-c",
                                "max_connections=500",
                            ],
                            "env_from": [{
                                "config_map_ref": {
                                    "name": "postgres-config",
                                },
                            }],
                            "image": "postgres:14",
                            "image_pull_policy": "IfNotPresent",
                            "name": "postgres",
                            "ports": [{
                                "container_port": 5432,
                            }],
                            "volume_mounts": [{
                                "mount_path": "/var/lib/postgresql/data",
                                "name": "postgres-data",
                                "sub_path": "postgres",
                            }],
                        }],
                        "volumes": [{
                            "name": "postgres-data",
                            "persistent_volume_claim": {
                                "claim_name": "postgres-pv-claim",
                            },
                        }],
                    },
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
