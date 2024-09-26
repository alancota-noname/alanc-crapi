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


class WorkshopArgs:
    def __init__(
        self,
        image: str = "491489166083.dkr.ecr.us-east-1.amazonaws.com/alanc-crapi-workshop-652e1cb:rc2",
        image_secret: str = "regcred",
        **kwargs,
    ):
        self.kwargs = kwargs
        self.image = image
        self.image_secret = image_secret

        for key, value in kwargs.items():
            setattr(self, key, value)


class Workshop(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: WorkshopArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        # -----------------------------------------#
        #             Workshop Service             #
        # -----------------------------------------#

        # Create Workshop ConfigMap
        self.workshop_config_map = ConfigMap(
            f"{settings.app_name}-{name}-ConfigMap",
            data={
                "DB_DRIVER": "postgres",
                "DB_HOST": "postgresdb",
                "DB_NAME": "crapi",
                "DB_PASSWORD": "crapisecretpassword",
                "DB_PORT": "5432",
                "DB_USER": "postgres",
                "IDENTITY_SERVICE": "crapi-identity:8080",
                "MONGO_DB_DRIVER": "mongodb",
                "MONGO_DB_HOST": "mongodb",
                "MONGO_DB_NAME": "crapi",
                "MONGO_DB_PASSWORD": "crapisecretpassword",
                "MONGO_DB_PORT": "27017",
                "MONGO_DB_USER": "admin",
                "SECRET_KEY": "crapi",
                "SERVER_PORT": "8000",
                "API_GATEWAY_URL": "https://api.mypremiumdealership.com",
                "TLS_ENABLED": "false",
                "TLS_CERTIFICATE": "certs / server.crt",
                "TLS_KEY": "certs / server.key",
            },
            metadata=MetadataBase(
                name=f"{name}-config",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="workshop",
                ),
            ),
            opts=opts,
        )

        # Create Workshop Service
        self.workshop_svc = Service(
            f"{settings.app_name}-{name}-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="workshop",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-python",
                        "port": 8000,
                    }
                ],
                "selector": {
                    "app": name,
                },
                "type": ServiceSpecType.CLUSTER_IP,
            },
            opts=opts,
        )

        # Community Deployment
        self.workshop = Deployment(
            f"{settings.app_name}-{name}-Deployment",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="workshop",
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
                                            "name": self.workshop_config_map.metadata.name,
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
                                        "container_port": 8000,
                                    }
                                ],
                                "readiness_probe": {
                                    "initial_delay_seconds": 15,
                                    "period_seconds": 10,
                                    "tcp_socket": {
                                        "port": 8000,
                                    },
                                },
                                "resources": {
                                    "limits": {
                                        "cpu": "256m",
                                    },
                                    "requests": {
                                        "cpu": "256m",
                                    },
                                },
                            }
                        ],
                        "init_containers": [
                            {
                                "args": [
                                    "service",
                                    "crapi-identity",
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-crapi-identity",
                            },
                            {
                                "args": [
                                    "service",
                                    "crapi-community",
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-crapi-community",
                            },
                        ],
                    },
                },
            },
            opts=opts,
        )

        # Pulumi Output registration
        self.register_outputs({})
