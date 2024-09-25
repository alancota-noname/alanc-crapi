import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class MailhogConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:MailhogConfigmap", name, {}, opts)

        mailhog_configmap = kubernetes.core.v1.ConfigMap(f"{name}-mailhogConfigmap",
            data={
                "MH_MONGO_URI": "admin:crapisecretpassword@mongodb:27017",
                "MH_STORAGE": "mongodb",
            },
            metadata={
                "labels": {
                    "app": "mailhog",
                },
                "name": "mailhog-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
