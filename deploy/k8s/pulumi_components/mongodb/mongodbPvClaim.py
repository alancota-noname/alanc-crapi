import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class MongodbPvClaim(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:MongodbPvClaim", name, {}, opts)

        mongodb_pv_claim = kubernetes.core.v1.PersistentVolumeClaim(f"{name}-mongodbPvClaim",
            metadata={
                "labels": {
                    "app": "mongo",
                },
                "name": "mongodb-pv-claim",
            },
            spec={
                "access_modes": ["ReadWriteOnce"],
                "resources": {
                    "requests": {
                        "storage": "1000Mi",
                    },
                },
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
