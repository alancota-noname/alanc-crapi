import pulumi

# Get some values from the Pulumi configuration (or use defaults)
config = pulumi.Config()


# ------------------------------------------------------#
#                 project settings                      #
# ------------------------------------------------------#

project_prefix = config.get("projectPrefix", "crapi")
project_version = config.get("projectVersion", "rc1")
project_unique_id = config.get("projectUniqueId", "crapi-rc1")
project_custom_resource_type = config.get(
    "projectCustomResourceType", "alanc:custom:crapi"
)

# ------------------------------------------------------#
#                   crapi settings                      #
# ------------------------------------------------------#

# Common App Labels and Metadata
# ------------------------------------------------------

app_name = config.get("appName", "crapi-app")
app_namespace = config.get("appNamespace", "crapi")

app_metadata_labels = {"app": app_name}
app_metadata_namespace = {"namespace": app_namespace}

# JWT Key File
jwt_key_file = config.get("jwtKeyFile")
app_jwt_key_name = config.get("appJwtKeyName", "jwt-key-secret")

# Databases
# ------------------------------------------------------

# MongoDB
app_mongodb_user = config.get("crapiMongodbUser", "admin")
app_mongodb_password = config.get("crapiMongodbPassword", "crapisecretpassword")
app_mongodb_host = config.get("crapiMongodbHost", "mongodb")
app_mongodb_port = config.get_int("crapiMongodbPort", 27017)
app_mongodb_db_name = config.get("crapiMongodbDbName", "crapi")
app_mongodb_image = config.get("crapiMongodbImage", "mongo:4.4")

# PostgresDB
app_postgresdb_user = config.get("crapiPostgresdbUser", "admin")
app_postgresdb_password = config.get("crapiPostgresdbPassword", "crapisecretpassword")
app_postgresdb_host = config.get("crapiPostgresdbHost", "postgresdb")
app_postgresdb_port = config.get_int("crapiPostgresdbPort", 5432)
app_postgresdb_db_name = config.get("crapiPostgresdbDbName", "crapi")
app_postgresdb_image = config.get("crapiPostgresdbImage", "postgres:14:4.4")
# ------------------------------------------------------#
