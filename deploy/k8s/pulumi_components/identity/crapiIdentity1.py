import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiIdentity1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiIdentity1", name, {}, opts)

        crapi_identity1 = kubernetes.core.v1.Service(f"{name}-crapiIdentity1",
            metadata={
                "labels": {
                    "app": "crapi-identity",
                },
                "name": "crapi-identity",
            },
            spec={
                "ports": [{
                    "name": "java",
                    "port": 8080,
                }],
                "selector": {
                    "app": "crapi-identity",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
