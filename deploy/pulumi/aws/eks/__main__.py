"""A Kubernetes Python Pulumi program"""

import pulumi
from config import settings
from utils.helpers import encode_file, k8s_labels
from pulumi_kubernetes.core.v1 import Namespace, Secret
from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from resources.databases import Database, DatabaseArgs
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

# 3 - Create the Databases

# Set the Pulumi custom component type
db_pulumi_component_type = (
    f"{settings.project_custom_resource_type}:{Database.__name__}"
)
# Create the MongoDB database
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
    args=DatabaseArgs(
        db_service=DatabaseServices.MONGODB,
        db_user=settings.app_mongodb_user,
        db_password=settings.app_mongodb_password,
        db_k8s_image=settings.app_mongodb_image,
    ),
)

# Create the PostgresDB database
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
    args=DatabaseArgs(
        db_service=DatabaseServices.POSTGRESDB,
        db_user=settings.app_postgresdb_user,
        db_port=settings.app_postgresdb_port,
        db_password=settings.app_postgresdb_password,
        db_name=settings.app_postgresdb_db_name,
        db_k8s_image=settings.app_postgresdb_image,
    ),
)

# Pulumi output exports

# Export the name of the namespace
# pulumi.export(
#     "namespace_name", app_namespace.metadata.apply(lambda metadata: metadata.name)
# )

# pulumi.export("jwt_key_secret", jwt_key.metadata["name"])
# pulumi.export("mongodb_config_map", mongodb.mongodb_config_map.metadata["name"])
# pulumi.export("mongodb_pvc", mongodb.mongodb_pvc.metadata["name"])
pulumi.export("mongodb", app_mongodb.mongodb.metadata["name"])
pulumi.export("postgresdb", app_postgresdb.postgresdb.metadata["name"])
