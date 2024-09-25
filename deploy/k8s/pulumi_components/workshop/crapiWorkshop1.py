import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWorkshop1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWorkshop1", name, {}, opts)

        crapi_workshop1 = kubernetes.core.v1.Service(f"{name}-crapiWorkshop1",
            metadata={
                "labels": {
                    "app": "crapi-workshop",
                },
                "name": "crapi-workshop",
            },
            spec={
                "ports": [{
                    "name": "python",
                    "port": 8000,
                }],
                "selector": {
                    "app": "crapi-workshop",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
