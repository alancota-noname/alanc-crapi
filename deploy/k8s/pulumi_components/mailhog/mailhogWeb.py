import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class MailhogWeb(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:MailhogWeb", name, {}, opts)

        mailhog_web = kubernetes.core.v1.Service(f"{name}-mailhogWeb",
            metadata={
                "name": "mailhog-web",
                "namespace": "crapi",
            },
            spec={
                "ports": [{
                    "name": "web",
                    "node_port": 30025,
                    "port": 8025,
                    "protocol": "TCP",
                }],
                "selector": {
                    "app": "mailhog",
                },
                "session_affinity": "None",
                "type": kubernetes.core.v1.ServiceSpecType.LOAD_BALANCER,
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
