import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiCommunityConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiCommunityConfigmap", name, {}, opts)

        crapi_community_configmap = kubernetes.core.v1.ConfigMap(f"{name}-crapiCommunityConfigmap",
            data={
                "DB_DRIVER": "postgres",
                "DB_HOST": "postgresdb",
                "DB_NAME": "crapi",
                "DB_PASSWORD": "crapisecretpassword",
                "DB_PORT": "5432",
                "DB_USER": "admin",
                "IDENTITY_SERVICE": "crapi-identity:8080",
                "MONGO_DB_DRIVER": "mongodb",
                "MONGO_DB_HOST": "mongodb",
                "MONGO_DB_NAME": "crapi",
                "MONGO_DB_PASSWORD": "crapisecretpassword",
                "MONGO_DB_PORT": "27017",
                "MONGO_DB_USER": "admin",
                "SERVER_PORT": "8087",
            },
            metadata={
                "labels": {
                    "app": "crapi-community",
                },
                "name": "crapi-community-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
