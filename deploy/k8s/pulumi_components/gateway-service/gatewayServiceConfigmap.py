import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class GatewayServiceConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:GatewayServiceConfigmap", name, {}, opts)

        gateway_service_configmap = kubernetes.core.v1.ConfigMap(f"{name}-gatewayServiceConfigmap",
            data={
                "SERVER_PORT": "443",
            },
            metadata={
                "labels": {
                    "app": "gateway-service",
                },
                "name": "gateway-service-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
