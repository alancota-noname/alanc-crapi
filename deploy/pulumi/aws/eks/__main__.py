"""A Kubernetes Python Pulumi program"""

import pulumi
from config import settings
from resources.bootstrap import Bootstrap
from resources.community import Community, CommunityArgs
from resources.web import WebArgs, Web
from resources.workshop import Workshop, WorkshopArgs
from utils.helpers import encode_file, k8s_labels
from pulumi_kubernetes.core.v1 import Namespace, Secret
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from resources.databases import Database, DatabaseArgs
from resources.mailhog import Mailhog, MailhogArgs
from resources.identity import Identity, IdentityArgs
from common.base import MetadataBase
from common.enums import DatabaseServices


# 1 - Create the Namespace
app_namespace = Namespace(
    resource_name=settings.app_namespace,
    metadata=ObjectMetaArgs(name=settings.app_namespace),
)

# 2 - Create the JWT Key Secret
jwt_key = Secret(
    resource_name=settings.app_jwt_key_name,
    metadata=ObjectMetaArgs(
        name=settings.app_jwt_key_name, namespace=settings.app_namespace
    ),
    string_data={"jwks.json": encode_file(settings.jwt_key_file)},
)

# Bootstrap the application
# Set the Pulumi custom component type
bootstrap_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Bootstrap.__name__}"
)
crapi_bootstrap = Bootstrap(
    name="rbac",
    type=bootstrap_pulumi_component_type,
    metadata=MetadataBase(
        name="rbac",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="rbac",
            component="bootstrap",
        ),
    ),
)

# 3 - Deploy the Databases

# Set the Pulumi custom component type
db_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Database.__name__}"
)
# Deploy the MongoDB database

mongodb_args = DatabaseArgs(
    db_service=DatabaseServices.MONGODB,
    db_user=settings.app_mongodb_user,
    db_port=settings.app_mongodb_port,
    db_password=settings.app_mongodb_password,
    db_k8s_image=settings.app_mongodb_image,
)

app_mongodb = Database(
    name="mongodb",
    type=db_pulumi_component_type,
    metadata=MetadataBase(
        name="mongodb",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="mongodb",
            component="database",
        ),
    ),
    args=mongodb_args,
)

# Deploy the PostgresDB database

postgres_args = DatabaseArgs(
    db_service=DatabaseServices.POSTGRESDB,
    db_user=settings.app_postgresdb_user,
    db_port=settings.app_postgresdb_port,
    db_password=settings.app_postgresdb_password,
    db_name=settings.app_postgresdb_db_name,
    db_host=settings.app_postgresdb_host,
    db_k8s_image=settings.app_postgresdb_image,
)

app_postgresdb = Database(
    name="postgresdb",
    type=db_pulumi_component_type,
    metadata=MetadataBase(
        name="postgresdb",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="postgresdb",
            component="database",
        ),
    ),
    args=postgres_args,
)

# Deploy the Mailhog app
# Set the Pulumi custom component type
email_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Mailhog.__name__}"
)

mailhog_args = MailhogArgs(
    host="mailhog",
    mongo_uri=settings.app_mailhog_mongo_uri,
    storage_host=settings.app_mailhog_storage,
    smtp_port=settings.app_mailhog_smtp_port,
    web_port=settings.app_mailhog_web_port,
    k8s_image=settings.app_mailhog_image,
    k8s_resource={
        "limits": {
            "cpu": "1",
            "memory": "1024Mi",
        },
        "requests": {
            "cpu": "50m",
            "memory": "64Mi",
        },
    },
)

app_mailhog = Mailhog(
    name="mailhog",
    type=email_pulumi_component_type,
    metadata=MetadataBase(
        name="mailhog",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="mailhog",
            component="mailhog",
        ),
    ),
    args=mailhog_args,
)

# Deploy the Identity app
# Set the Pulumi custom component type
identity_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Identity.__name__}"
)

identity_args = IdentityArgs(
    jwt_expiration=settings.app_identity_jwt_expiration,
    jwt_secret=settings.app_identity_jwt_secret,
    registration_email_domain=settings.app_identity_registration_email_domain,
    postgres_args=postgres_args,
    mailhog_args=mailhog_args,
    image=settings.app_identity_image,
    image_secret=settings.app_identity_image_secret,
    k8s_resource={
        "limits": {
            "cpu": "500m",
        },
        "requests": {
            "cpu": "256m",
        },
    },
)

app_identity = Identity(
    name="crapi-identity",
    type=identity_pulumi_component_type,
    metadata=MetadataBase(
        name="crapi-identity",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="crapi-identity",
            component="identity",
        ),
    ),
    args=identity_args,
)

# Community Deployment

community_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Community.__name__}"
)

community_args = CommunityArgs(
    k8s_resource={
        "limits": {
            "cpu": "500m",
        },
        "requests": {
            "cpu": "256m",
        },
    },
)

app_community = Community(
    name="crapi-community",
    type=community_pulumi_component_type,
    metadata=MetadataBase(
        name="crapi-community",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="crapi-community",
            component="community",
        ),
    ),
    args=community_args,
)

# Workshop Deployment
workshop_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Workshop.__name__}"
)

workshop_args = WorkshopArgs(
    k8s_resource={
        "limits": {
            "cpu": "500m",
        },
        "requests": {
            "cpu": "256m",
        },
    },
)

app_workshop = Workshop(
    name="crapi-workshop",
    type=workshop_pulumi_component_type,
    metadata=MetadataBase(
        name="crapi-workshop",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="crapi-workshop",
            component="workshop",
        ),
    ),
    args=workshop_args,
)

# Web Deployment
web_pulumi_component_type = f"{settings.project_custom_resource_type}:{Web.__name__}"

web_args = WebArgs(
    k8s_resource={
        "limits": {
            "cpu": "500m",
        },
        "requests": {
            "cpu": "256m",
        },
    },
)

app_web = Web(
    name="crapi-web",
    type=web_pulumi_component_type,
    metadata=MetadataBase(
        name="crapi-web",
        namespace=settings.app_namespace,
        labels=k8s_labels(
            name="crapi-web",
            component="web",
        ),
    ),
    args=web_args,
)


# Pulumi output exports
pulumi.export("namespace", app_namespace.metadata["name"])
pulumi.export("jwt_key", jwt_key.metadata["name"])
pulumi.export("service_account", crapi_bootstrap.service_account.metadata["name"])
pulumi.export("cluster_role", crapi_bootstrap.cluster_role.metadata["name"])
pulumi.export("role_binding", crapi_bootstrap.role_binding.metadata["name"])
pulumi.export("mongodb", app_mongodb.mongodb.metadata["name"])
pulumi.export("postgresdb", app_postgresdb.postgresdb.metadata["name"])
pulumi.export("mailhog", app_mailhog.mailhog.metadata["name"])
pulumi.export("identity", app_identity.identity.metadata["name"])
pulumi.export("community", app_community.community.metadata["name"])
pulumi.export("workshop", app_workshop.workshop.metadata["name"])
pulumi.export("web", app_web.web.metadata["name"])
#
