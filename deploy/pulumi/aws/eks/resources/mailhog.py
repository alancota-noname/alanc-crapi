from typing import Any

from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.core.v1 import ConfigMap, Service, ServiceSpecType
from pulumi_kubernetes.apps.v1 import Deployment
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from common.base import MetadataBase

from config import settings
from utils.helpers import k8s_labels


class MailhogArgs:
    def __init__(
        self,
        host: str,
        mongo_uri: str,
        storage_host: str,
        smtp_port: int,
        web_port: int,
        k8s_image: str,
        k8s_resource: dict[str, Any],
        **kwargs,
    ):
        self.host = host
        self.mongo_uri = mongo_uri
        self.storage_host = storage_host
        self.smtp_port = smtp_port
        self.web_port = web_port
        self.k8s_image = k8s_image
        self.k8s_resource = k8s_resource
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)


class Mailhog(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: MailhogArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        print(f"Type: {type}")

        # Create Mailhog ConfigMap
        self.mailhog_config_map = ConfigMap(
            f"{settings.app_name}-{name}-ConfigMap",
            data={
                "MH_MONGO_URI": args.mongo_uri,
                "MH_STORAGE": args.storage_host,
            },
            metadata=MetadataBase(
                name=f"{name}-config",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="mailhog",
                ),
            ),
            opts=opts,
        )

        # Create Mailhog SMTP Service
        self.mailhog_smtp_svc = Service(
            f"{settings.app_name}-{name}-smtp-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="mailhog",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-smtp",
                        "port": args.smtp_port,
                        "protocol": "TCP",
                        "target_port": args.smtp_port,
                    }
                ],
                "selector": {
                    "app": name,
                },
                "session_affinity": "None",
                "type": ServiceSpecType.CLUSTER_IP,
            },
            opts=opts,
        )

        # Create Mailhog Web Service
        self.mailhog_web_svc = Service(
            f"{settings.app_name}-{name}-web-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="mailhog",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-web",
                        "port": args.web_port,
                        "protocol": "TCP",
                        "target_port": args.web_port,
                    }
                ],
                "selector": {
                    "app": name,
                },
                "session_affinity": "None",
                "type": ServiceSpecType.CLUSTER_IP,
            },
            opts=opts,
        )

        # Create Mailhog Deployment
        self.mailhog = Deployment(
            f"{settings.app_name}-{name}-Deployment",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="mailhog",
                ),
            ),
            spec={
                "min_ready_seconds": 10,
                "progress_deadline_seconds": 600,
                "replicas": 1,
                "selector": {
                    "match_labels": {
                        "app": name,
                    },
                },
                "template": {
                    "metadata": {
                        "annotations": {
                            "sidecar_traceable_ai_inject": "false",
                        },
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
                                            "name": self.mailhog_config_map.metadata[
                                                "name"
                                            ],
                                        },
                                    }
                                ],
                                "image": args.k8s_image,
                                "image_pull_policy": "Always",
                                "image_pull_secrets": [
                                    {
                                        "name": "regcred",
                                    }
                                ],
                                "liveness_probe": {
                                    "initial_delay_seconds": 15,
                                    "period_seconds": 60,
                                    "tcp_socket": {
                                        "port": args.smtp_port,
                                    },
                                },
                                "name": name,
                                "ports": [
                                    {
                                        "container_port": args.web_port,
                                        "name": f"{name}-web",
                                        "protocol": "TCP",
                                    },
                                    {
                                        "container_port": args.smtp_port,
                                        "name": f"{name}-smtp",
                                        "protocol": "TCP",
                                    },
                                ],
                                "readiness_probe": {
                                    "initial_delay_seconds": 15,
                                    "period_seconds": 20,
                                    "tcp_socket": {
                                        "port": 1025,
                                    },
                                },
                                "resources": args.k8s_resource,
                            }
                        ],
                        "security_context": {
                            "run_as_group": 0,
                            "run_as_user": 0,
                        },
                    },
                },
            },
            opts=opts,
        )

        # Pulumi Output registration
        self.register_outputs({})
