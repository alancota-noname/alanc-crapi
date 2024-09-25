import pulumi
from pulumi import Input
from typing import Optional, Dict, TypedDict, Any
import pulumi_kubernetes as kubernetes

class CrapiWebConfigmap(pulumi.ComponentResource):
    def __init__(self, name: str, opts: Optional[pulumi.ResourceOptions] = None):
        super().__init__("components:index:CrapiWebConfigmap", name, {}, opts)

        crapi_web_configmap = kubernetes.core.v1.ConfigMap(f"{name}-crapiWebConfigmap",
            data={
                "COMMUNITY_SERVICE": "crapi-community:8087",
                "IDENTITY_SERVICE": "crapi-identity:8080",
                "WORKSHOP_SERVICE": "crapi-workshop:8000",
            },
            metadata={
                "labels": {
                    "app": "crapi-web",
                },
                "name": "crapi-web-configmap",
            },
            opts = pulumi.ResourceOptions(parent=self))

        self.register_outputs()
