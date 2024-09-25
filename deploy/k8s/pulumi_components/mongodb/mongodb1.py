import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Mongodb1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Mongodb1", name, {}, opts)

        mongodb1 = kubernetes.apps.v1.StatefulSet(f"{name}-mongodb1",
            metadata={
                "name": "mongodb",
            },
            spec={
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": "mongodb",
                    },
                },
                "service_name": "mongodb",
                "template": {
                    "metadata": {
                        "labels": {
                            "app": "mongodb",
                        },
                    },
                    "spec": {
                        "containers": [{
                            "env_from": [{
                                "config_map_ref": {
                                    "name": "mongodb-config",
                                },
                            }],
                            "image": "mongo:4.4",
                            "image_pull_policy": "IfNotPresent",
                            "name": "mongodb",
                            "volume_mounts": [{
                                "mount_path": "/data/db",
                                "name": "mongodb-data",
                            }],
                        }],
                        "volumes": [{
                            "name": "mongodb-data",
                            "persistent_volume_claim": {
                                "claim_name": "mongodb-pv-claim",
                            },
                        }],
                    },
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
