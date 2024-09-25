import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class WaitforGrant(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:WaitforGrant", name, {}, opts)

        waitfor_grant = kubernetes.rbac.v1.ClusterRoleBinding(f"{name}-waitforGrant",
            metadata={
                "name": "waitfor-grant",
                "namespace": "crapi",
            },
            role_ref={
                "api_group": "",
                "kind": "ClusterRole",
                "name": "waitfor-reader",
            },
            subjects=[{
                "api_group": "",
                "kind": "ServiceAccount",
                "name": "default",
                "namespace": "crapi",
            }],
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
