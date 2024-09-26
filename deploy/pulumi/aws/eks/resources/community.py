from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.core.v1 import (
    ConfigMap,
    Service,
    ServiceSpecType,
)
from pulumi_kubernetes.apps.v1 import Deployment
from common.base import MetadataBase
from config import settings
from utils.helpers import k8s_labels


class CommunityArgs:
    def __init__(
        self,
        image: str = "491489166083.dkr.ecr.us-east-1.amazonaws.com/alanc-crapi-community-1905b0e:rc2",
        image_secret: str = "regcred",
        **kwargs,
    ):
        self.image = image
        self.image_secret = image_secret
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)


class Community(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: CommunityArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        # -----------------------------------------#
        #             Community Service            #
        # -----------------------------------------#

        # Create Community ConfigMap
        self.community_config_map = ConfigMap(
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
                "SERVER_PORT": "8087",
            },
            metadata=MetadataBase(
                name=f"{name}-config",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="community",
                ),
            ),
            opts=opts,
        )

        # Create Community Service
        self.community_svc = Service(
            f"{settings.app_name}-{name}-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="community",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-go",
                        "port": 8087,
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
        self.community = Deployment(
            f"{settings.app_name}-{name}-Deployment",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="community",
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
                                            "name": self.community_config_map.metadata.name,
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
                                        "container_port": 8087,
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
                        "init_containers": [
                            {
                                "args": [
                                    "service",
                                    "postgresdb",
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-postgres",
                            },
                            {
                                "args": [
                                    "service",
                                    "mongodb",
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-mongo",
                            },
                            {
                                "args": [
                                    "service",
                                    "crapi-identity",
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-java",
                            },
                        ],
                    },
                },
            },
            opts=opts,
        )

        # Pulumi Output registration
        self.register_outputs({})
