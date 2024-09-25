import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Postgresdb(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Postgresdb", name, {}, opts)

        postgresdb = kubernetes.core.v1.Service(f"{name}-postgresdb",
            metadata={
                "labels": {
                    "app": "postgresdb",
                },
                "name": "postgresdb",
            },
            spec={
                "ports": [{
                    "name": "postgres",
                    "port": 5432,
                }],
                "selector": {
                    "app": "postgresdb",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
