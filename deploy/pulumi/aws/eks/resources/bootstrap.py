from pulumi import ComponentResource, ResourceOptions
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from pulumi_kubernetes.rbac.v1 import ClusterRole, ClusterRoleBinding
from pulumi_kubernetes.core.v1 import ServiceAccount

from common.base import MetadataBase
from config import settings
from utils.helpers import k8s_labels


# Necessary for the health checks to communicate with the Kubernetes API


class Bootstrap(ComponentResource):
    def __init__(
        self,
        name: str,
        type: str,
        opts: ResourceOptions = None,
        metadata: ObjectMetaArgs = None,
    ):
        super().__init__(type, name, {}, opts)

        # -----------------------------------------#
        #        Role Based Access Control         #
        # -----------------------------------------#

        self.service_account = ServiceAccount(
            f"{settings.app_name}-{name}-ServiceAccount",
            metadata=MetadataBase(
                name=f"{name}-service-account",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="bootstrap",
                ),
            ),
        )

        # Create the Role
        self.cluster_role = ClusterRole(
            f"{settings.app_name}-{name}-ClusterRole",
            metadata=MetadataBase(
                name=f"{name}-cluster-role",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="bootstrap",
                ),
            ),
            rules=[
                {
                    "api_groups": [""],
                    "resources": [
                        "services",
                        "pods",
                    ],
                    "verbs": [
                        "get",
                        "watch",
                        "list",
                    ],
                }
            ],
        )

        # Create the Role Binding
        self.role_binding = ClusterRoleBinding(
            f"{settings.app_name}-{name}-ClusterRoleBinding",
            metadata=MetadataBase(
                name=f"{name}-cluster-role-binding",
                namespace=settings.app_namespace,
                labels=k8s_labels(
                    name=name,
                    component="bootstrap",
                ),
            ),
            role_ref={
                "api_group": "",
                "kind": "ClusterRole",
                "name": self.cluster_role.metadata.name,
            },
            subjects=[
                {
                    "api_group": "",
                    "kind": "ServiceAccount",
                    "name": "default",
                    "namespace": settings.app_namespace,
                }
            ],
        )
