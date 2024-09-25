import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class GatewayService1(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:GatewayService1", name, {}, opts)

        gateway_service1 = kubernetes.core.v1.Service(f"{name}-gatewayService1",
            metadata={
                "labels": {
                    "app": "gateway-service",
                },
                "name": "gateway-service",
            },
            spec={
                "ports": [{
                    "name": "go",
                    "port": 8087,
                }],
                "selector": {
                    "app": "gateway-service",
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
