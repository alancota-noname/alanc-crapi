import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class MongodbConfig(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:MongodbConfig", name, {}, opts)

        mongodb_config = kubernetes.core.v1.ConfigMap(f"{name}-mongodbConfig",
            data={
                "MONGO_INITDB_ROOT_PASSWORD": "crapisecretpassword",
                "MONGO_INITDB_ROOT_USERNAME": "admin",
            },
            metadata={
                "labels": {
                    "app": "mongodb",
                },
                "name": "mongodb-config",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
