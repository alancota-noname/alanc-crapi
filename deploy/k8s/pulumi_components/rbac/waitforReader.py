import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class WaitforReader(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:WaitforReader", name, {}, opts)

        waitfor_reader = kubernetes.rbac.v1.ClusterRole(f"{name}-waitforReader",
            metadata={
                "name": "waitfor-reader",
                "namespace": "crapi",
            },
            rules=[{
                "api_groups": [""],
                "resources": [
                    "services",
                    "pods",
                ],
                "verbs": [
                    "get",
                    "watch",
                    "list",
                ],
            }],
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
