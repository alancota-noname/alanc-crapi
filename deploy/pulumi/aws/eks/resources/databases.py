from typing import Any

from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.core.v1 import ConfigMap, PersistentVolumeClaim, Service
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.apps.v1 import StatefulSet
from common.base import MetadataBase
from common.enums import DatabaseServices

from config import settings
from utils.helpers import k8s_labels


class DatabaseArgs:
    def __init__(
        self,
        db_service: DatabaseServices,
        db_user: str,
        db_password: str,
        db_k8s_image: str,
        db_name: str | None = None,
        db_host: str | None = None,
        db_port: int | None = None,
        db_k8s_pvc_size: str | None = "1000Mi",
        db_k8s_pvc_storage_class: str | None = None,
        db_k8s_pvc_annotations: dict[str, Any] | None = None,
        db_k8s_replicas: int | None = 1,
        db_k8s_resources: dict[str, Any] | None = None,
        **kwargs,
    ):
        self.db_service = db_service
        self.db_name = db_name
        self.db_user = db_user
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_k8s_pvc_size = db_k8s_pvc_size
        self.db_k8s_pvc_storage_class = db_k8s_pvc_storage_class
        self.db_k8s_pvc_annotations = db_k8s_pvc_annotations
        self.db_k8s_replicas = db_k8s_replicas
        self.db_k8s_resources = db_k8s_resources
        self.db_k8s_image = db_k8s_image
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)


class Database(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: DatabaseArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        print(f"Type: {type}")

        # -----------------------------------------#
        #                 Mongo DB                 #
        # -----------------------------------------#

        if args.db_service == DatabaseServices.MONGODB:
            # Create MongoDB ConfigMap
            self.mongodb_config_map = ConfigMap(
                f"{settings.app_name}-{name}-ConfigMap",
                data={
                    "MONGO_INITDB_ROOT_PASSWORD": args.db_password,
                    "MONGO_INITDB_ROOT_USERNAME": args.db_user,
                },
                metadata=MetadataBase(
                    name=f"{name}-config",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                opts=opts,
            )

            # Create MongoDB Persistent Volume Claim
            self.mongodb_pvc = PersistentVolumeClaim(
                f"{settings.app_name}-{name}-PVC",
                metadata=MetadataBase(
                    name=f"{name}-pvc",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                spec={
                    "access_modes": ["ReadWriteOnce"],
                    "resources": {
                        "requests": {
                            "storage": args.db_k8s_pvc_size,
                        },
                    },
                },
                opts=opts,
            )

            # MongoDB StatefulSet Deployment
            self.mongodb = StatefulSet(
                f"{settings.app_name}-{name}-StatefulSet",
                metadata=MetadataBase(
                    name=f"{name}-statefulset",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                spec={
                    "replicas": args.db_k8s_replicas,
                    "selector": {
                        "match_labels": {
                            "app": name,
                        },
                    },
                    "service_name": settings.app_mongodb_host,
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
                                                "name": self.mongodb_config_map.metadata[
                                                    "name"
                                                ],
                                            },
                                        }
                                    ],
                                    "image": args.db_k8s_image,
                                    "image_pull_policy": "IfNotPresent",
                                    "name": name,
                                    "volume_mounts": [
                                        {
                                            "mount_path": "/data/db",
                                            "name": f"{name}-data",
                                        }
                                    ],
                                }
                            ],
                            "volumes": [
                                {
                                    "name": f"{name}-data",
                                    "persistent_volume_claim": {
                                        "claim_name": self.mongodb_pvc.metadata["name"],
                                    },
                                }
                            ],
                        },
                    },
                },
                opts=opts,
            )

        # -----------------------------------------#
        #                 Postgres                 #
        # -----------------------------------------#

        if args.db_service == DatabaseServices.POSTGRESDB:
            # Create Postgres ConfigMap
            self.postgres_config_map = ConfigMap(
                f"{settings.app_name}-{name}-ConfigMap",
                data={
                    "POSTGRES_PASSWORD": args.db_password,
                    "POSTGRES_USERNAME": args.db_user,
                    "POSTGRES_DB": args.db_name,
                },
                metadata=MetadataBase(
                    name=f"{name}-config",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                opts=opts,
            )

            # Create Postgres Persistent Volume Claim
            self.postgres_pvc = PersistentVolumeClaim(
                f"{settings.app_name}-{name}-PVC",
                metadata=MetadataBase(
                    name=f"{name}-pvc",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                spec={
                    "access_modes": ["ReadWriteOnce"],
                    "resources": {
                        "requests": {
                            "storage": args.db_k8s_pvc_size,
                        },
                    },
                },
                opts=opts,
            )

            # Create Postgres Service
            self.postgres_svc = Service(
                f"{settings.app_name}-{name}-Service",
                metadata=MetadataBase(
                    name=name,
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                spec={
                    "ports": [
                        {
                            "name": name,
                            "port": args.db_port,
                        }
                    ],
                    "selector": {
                        "app": name,
                    },
                },
                opts=opts,
            )

            # Postgres StatefulSet Deployment
            self.postgresdb = StatefulSet(
                f"{settings.app_name}-{name}-StatefulSet",
                metadata=MetadataBase(
                    name=f"{name}-statefulset",
                    namespace=settings.app_namespace,
                    labels=k8s_labels(
                        name=name,
                        component="database",
                    ),
                ),
                spec={
                    "replicas": args.db_k8s_replicas,
                    "selector": {
                        "match_labels": {
                            "app": name,
                        },
                    },
                    "service_name": settings.app_postgresdb_host,
                    "template": {
                        "metadata": {
                            "labels": {
                                "app": name,
                            },
                        },
                        "spec": {
                            "containers": [
                                {
                                    "args": [
                                        "-c",
                                        "max_connections=500",
                                    ],
                                    "env_from": [
                                        {
                                            "config_map_ref": {
                                                "name": self.postgres_config_map.metadata[
                                                    "name"
                                                ],
                                            },
                                        }
                                    ],
                                    "image": args.db_k8s_image,
                                    "image_pull_policy": "IfNotPresent",
                                    "name": name,
                                    "ports": [
                                        {
                                            "container_port": args.db_port,
                                        }
                                    ],
                                    "volume_mounts": [
                                        {
                                            "mount_path": "/var/lib/postgresql/data",
                                            "name": f"{name}-data",
                                            "sub_path": name,
                                        }
                                    ],
                                }
                            ],
                            "volumes": [
                                {
                                    "name": f"{name}-data",
                                    "persistent_volume_claim": {
                                        "claim_name": self.postgres_pvc.metadata[
                                            "name"
                                        ],
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
