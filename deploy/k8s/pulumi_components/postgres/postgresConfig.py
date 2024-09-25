import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class PostgresConfig(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:PostgresConfig", name, {}, opts)

        postgres_config = kubernetes.core.v1.ConfigMap(f"{name}-postgresConfig",
            data={
                "POSTGRES_DB": "crapi",
                "POSTGRES_PASSWORD": "crapisecretpassword",
                "POSTGRES_USER": "admin",
            },
            metadata={
                "labels": {
                    "app": "postgresdb",
                },
                "name": "postgres-config",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
