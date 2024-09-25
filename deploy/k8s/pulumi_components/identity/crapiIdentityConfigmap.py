import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiIdentityConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiIdentityConfigmap", name, {}, opts)

        crapi_identity_configmap = kubernetes.core.v1.ConfigMap(f"{name}-crapiIdentityConfigmap",
            data={
                "APP_NAME": "crapi-identity",
                "DB_DRIVER": "postgresql",
                "DB_HOST": "postgresdb",
                "DB_NAME": "crapi",
                "DB_PASSWORD": "crapisecretpassword",
                "DB_PORT": "5432",
                "DB_USER": "admin",
                "ENABLE_LOG4J": "true",
                "ENABLE_SHELL_INJECTION": "false",
                "JWT_EXPIRATION": "604800000",
                "JWT_SECRET": "crapi",
                "MAILHOG_DOMAIN": "example.com",
                "MAILHOG_HOST": "mailhog",
                "MAILHOG_PORT": "1025",
                "SERVER_PORT": "8080",
                "SMTP_AUTH": "true",
                "SMTP_EMAIL": "user@example.com",
                "SMTP_FROM": "no-reply@example.com",
                "SMTP_HOST": "smtp.example.com",
                "SMTP_PASS": "xxxxxxxxxxxxxx",
                "SMTP_PORT": "587",
                "SMTP_STARTTLS": "true",
            },
            metadata={
                "labels": {
                    "app": "crapi-identity",
                },
                "name": "crapi-identity-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
