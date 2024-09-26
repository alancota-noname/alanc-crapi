from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.core.v1 import ConfigMap

from common.base import MetadataBase
from config import settings
from utils.helpers import k8s_labels
from pulumi_kubernetes.core.v1 import (
    Service,
    ServiceSpecType,
)
from pulumi_kubernetes.apps.v1 import Deployment


class WebArgs:
    def __init__(
        self,
        image: str = "491489166083.dkr.ecr.us-east-1.amazonaws.com/alanc-crapi-web-6deb260:rc2",
        image_secret: str = "regcred",
        **kwargs,
    ):
        self.kwargs = kwargs
        self.image = image
        self.image_secret = image_secret

        for key, value in kwargs.items():
            setattr(self, key, value)


class Web(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: WebArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        # -----------------------------------------#
        #             Web Service             #
        # -----------------------------------------#

        # Create Web ConfigMap
        self.web_config_map = ConfigMap(
            f"{settings.app_name}-{name}-ConfigMap",
            data={
                "COMMUNITY_SERVICE": "crapi-community:8087",
                "IDENTITY_SERVICE": "crapi-identity:8080",
                "WORKSHOP_SERVICE": "crapi-workshop:8000",
                "MAILHOG_WEB_SERVICE": "mailhog:8025",
                "TLS_ENABLED": "false",
            },
            metadata=MetadataBase(
                name=f"{name}-config",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="web",
                ),
            ),
            opts=opts,
        )

        # Create Web Service
        self.web_svc = Service(
            f"{settings.app_name}-{name}-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="web",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-nginx",
                        "node_port": 30081,
                        "port": 80,
                    }
                ],
                "selector": {
                    "app": name,
                },
                "type": ServiceSpecType.NODE_PORT,
            },
            opts=opts,
        )

        # Community Deployment
        self.web = Deployment(
            f"{settings.app_name}-{name}-Deployment",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="web",
                ),
            ),
            spec={
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": name,
                    },
                },
                "template": {
                    "metadata": {
                        "labels": {
                            "app": name,
                        },
                    },
                    "spec": {
                        "containers": [
                            {
                                "env_from": [
                                    {
                                        "config_map_ref": {
                                            "name": self.web_config_map.metadata.name,
                                        },
                                    }
                                ],
                                "image": args.image,
                                "image_pull_policy": "Always",
                                "image_pull_secrets": [
                                    {
                                        "name": args.image_secret,
                                    }
                                ],
                                "name": name,
                                "ports": [
                                    {
                                        "container_port": 80,
                                    }
                                ],
                                "resources": {
                                    "limits": {
                                        "cpu": "500m",
                                    },
                                    "requests": {
                                        "cpu": "256m",
                                    },
                                },
                            }
                        ],
                    },
                },
            },
            opts=opts,
        )

        # Pulumi Output registration
        self.register_outputs({})
