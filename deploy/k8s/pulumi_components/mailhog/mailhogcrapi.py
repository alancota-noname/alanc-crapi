import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class Mailhogcrapi(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:Mailhogcrapi", name, {}, opts)

        mailhogcrapi = kubernetes.core.v1.Service(f"{name}-mailhogcrapi",
            metadata={
                "name": "mailhog",
                "namespace": "crapi",
            },
            spec={
                "ports": [{
                    "name": "smtp",
                    "port": 1025,
                    "protocol": "TCP",
                    "target_port": 1025,
                }],
                "selector": {
                    "app": "mailhog",
                },
                "session_affinity": "None",
                "type": kubernetes.core.v1.ServiceSpecType.CLUSTER_IP,
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
