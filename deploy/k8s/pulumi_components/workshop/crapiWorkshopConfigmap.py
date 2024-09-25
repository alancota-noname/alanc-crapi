import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWorkshopConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWorkshopConfigmap", name, {}, opts)

        crapi_workshop_configmap = kubernetes.core.v1.ConfigMap(f"{name}-crapiWorkshopConfigmap",
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
                "SECRET_KEY": "crapi",
                "SERVER_PORT": "8000",
            },
            metadata={
                "labels": {
                    "app": "crapi-workshop",
                },
                "name": "crapi-workshop-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
