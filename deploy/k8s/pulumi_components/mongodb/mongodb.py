import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Mongodb(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Mongodb", name, {}, opts)

        mongodb = kubernetes.core.v1.Service(f"{name}-mongodb",
            metadata={
                "labels": {
                    "app": "mongodb",
                },
                "name": "mongodb",
            },
            spec={
                "ports": [{
                    "name": "mongo",
                    "port": 27017,
                }],
                "selector": {
                    "app": "mongodb",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
