import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiCommunity1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiCommunity1", name, {}, opts)

        crapi_community1 = kubernetes.core.v1.Service(f"{name}-crapiCommunity1",
            metadata={
                "labels": {
                    "app": "crapi-community",
                },
                "name": "crapi-community",
            },
            spec={
                "ports": [{
                    "name": "go",
                    "port": 8087,
                }],
                "selector": {
                    "app": "crapi-community",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
