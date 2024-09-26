from typing import Any

from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.core.v1 import ConfigMap, Service
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.apps.v1 import Deployment
from resources.databases import DatabaseArgs
from resources.mailhog import MailhogArgs
from common.base import MetadataBase

from config import settings
from utils.helpers import k8s_labels


class IdentityArgs:
    def __init__(
        self,
        jwt_expiration: str,
        jwt_secret: str,
        registration_email_domain: str,
        image: str,
        k8s_resource: dict[str, Any],
        image_secret: str | None = None,
        enable_shell_injection: bool = False,
        enable_log4j: bool = True,
        server_port: int = 8080,
        mailhog_args: MailhogArgs | None = None,
        postgres_args: DatabaseArgs | None = None,
        k8s_replicas: int | None = 1,
        **kwargs,
    ):
        self.image = image
        self.image_secret = image_secret
        self.enable_shell_injection = enable_shell_injection
        self.enable_log4j = enable_log4j
        self.jwt_expiration = jwt_expiration
        self.jwt_secret = jwt_secret
        self.registration_email_domain = registration_email_domain
        self.server_port = server_port
        self.mailhog_args = mailhog_args
        self.postgres_args = postgres_args
        self.k8s_replicas = k8s_replicas
        self.k8s_resource = k8s_resource
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)


class Identity(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        args: IdentityArgs | None,
        opts: [ResourceOptions] = None,
        metadata: ObjectMetaArgs | None = None,
    ):
        super().__init__(type, name, {}, opts)

        # -----------------------------------------#
        #             Identity Service             #
        # -----------------------------------------#

        # Create Identity ConfigMap
        self.identity_config_map = ConfigMap(
            f"{settings.app_name}-{name}-ConfigMap",
            data={
                "APP_NAME": name,
                "LOG_LEVEL": "DEBUG",
                "DB_DRIVER": "postgresql",
                "DB_HOST": args.postgres_args.db_host,
                "DB_NAME": args.postgres_args.db_name,
                "DB_PASSWORD": args.postgres_args.db_password,
                "DB_PORT": f"{args.postgres_args.db_port}",
                "DB_USER": f"{args.postgres_args.db_user}",
                "ENABLE_LOG4J": f"{args.enable_log4j}",
                "ENABLE_SHELL_INJECTION": f"{args.enable_shell_injection}",
                "JWT_EXPIRATION": args.jwt_expiration,
                "JWT_SECRET": args.jwt_secret,
                "MAILHOG_DOMAIN": args.registration_email_domain,
                "MAILHOG_HOST": args.mailhog_args.host,
                "MAILHOG_PORT": f"{args.mailhog_args.smtp_port}",
                "SERVER_PORT": f"{args.server_port}",
                "SMTP_FROM": f"no-reply@{args.registration_email_domain}",
                "API_GATEWAY_URL": "https://api.mypremiumdealership.com",
                "TLS_ENABLED": "false",
                "TLS_KEYSTORE_TYPE": "PKCS12",
                "TLS_KEYSTORE": "classpath:certs/server.p12",
                "TLS_KEYSTORE_PASSWORD": "passw0rd",
                "TLS_KEY_PASSWORD": "passw0rd",
                "TLS_KEY_ALIAS": "identity",
                # Ignored for now
                "SMTP_AUTH": "true",
                "SMTP_EMAIL": "user@example.com",
                "SMTP_HOST": "smtp.example.com",
                "SMTP_PASS": "xxxxxxxxxxxxxx",
                "SMTP_PORT": "587",
                "SMTP_STARTTLS": "true",
            },
            metadata=MetadataBase(
                name=f"{name}-config",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="identity",
                ),
            ),
            opts=opts,
        )

        # Create Identity Service
        self.identity_svc = Service(
            f"{settings.app_name}-{name}-Service",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="identity",
                ),
            ),
            spec={
                "ports": [
                    {
                        "name": f"{name}-java",
                        "port": args.server_port,
                    }
                ],
                "selector": {
                    "app": name,
                },
            },
            opts=opts,
        )

        # Create Identity Deployment
        self.identity = Deployment(
            f"{settings.app_name}-{name}-Deployment",
            metadata=MetadataBase(
                name=name,
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="identity",
                ),
            ),
            spec={
                "replicas": args.k8s_replicas,
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
                                            "name": self.identity_config_map.metadata[
                                                "name"
                                            ],
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
                                        "container_port": args.server_port,
                                    }
                                ],
                                "readiness_probe": {
                                    "initial_delay_seconds": 15,
                                    "period_seconds": 10,
                                    "tcp_socket": {
                                        "port": args.server_port,
                                    },
                                },
                                "resources": args.k8s_resource,
                                "volume_mounts": [
                                    {
                                        "mount_path": "/.keys",
                                        "name": "jwt-key-secret",
                                        "read_only": True,
                                    }
                                ],
                            }
                        ],
                        "init_containers": [
                            {
                                "args": [
                                    "service",
                                    args.postgres_args.db_host,
                                ],
                                "image": "groundnuty/k8s-wait-for:v1.3",
                                "image_pull_policy": "Always",
                                "name": "wait-for-postgres",
                            }
                        ],
                        "volumes": [
                            {
                                "name": "jwt-key-secret",
                                "secret": {
                                    "secret_name": "jwt-key-secret",
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
