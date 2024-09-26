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

# Email - Mailhog
# ------------------------------------------------------
app_mailhog_smtp_port = config.get_int("crapiEmailSmtpPort", 1025)
app_mailhog_web_port = config.get_int("crapiEmailWebPort", 8025)
app_mailhog_storage = config.get("crapiEmailStorageService", "mongodb")
app_mailhog_mongo_uri = config.get(
    "crapiEmailStorageUri", "admin:crapisecretpassword@mongodb:27017"
)
app_mailhog_image = config.get("crapiEmailImage", "crapi/mailhog:latest")

# Identity Service
# ------------------------------------------------------
app_identity_server_host = config.get("crapiIdentityServerHost", "crapi-identity")
app_identity_server_port = config.get_int("crapiIdentityServerPort", 8080)
app_identity_enable_log4j = config.get_bool("crapiIdentityEnableLog4j", True)
app_identity_enable_shell_injection = config.get_bool(
    "crapiIdentityEnableShellInjection", False
)
app_identity_jwt_expiration = config.get("crapiIdentityJwtExpiration", "604800000")
app_identity_jwt_secret = config.get("crapiIdentityJwtSecret", "crapi")
app_identity_registration_email_domain = config.get(
    "crapiIdentityMailhogDomain", "example.com"
)
app_identity_image = config.get("crapiIdentityImage", "crapi/identity:latest")
app_identity_image_secret = config.get("crapiIdentityImageSecret", "regcred")
