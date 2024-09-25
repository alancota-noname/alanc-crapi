import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWeb1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWeb1", name, {}, opts)

        crapi_web1 = kubernetes.core.v1.Service(f"{name}-crapiWeb1",
            metadata={
                "labels": {
                    "app": "crapi-web",
                },
                "name": "crapi-web",
            },
            spec={
                "ports": [{
                    "name": "nginx",
                    "node_port": 30080,
                    "port": 80,
                }],
                "selector": {
                    "app": "crapi-web",
                },
                "type": kubernetes.core.v1.ServiceSpecType.LOAD_BALANCER,
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
