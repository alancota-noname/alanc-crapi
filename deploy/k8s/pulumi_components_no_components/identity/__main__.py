import pulumi
import pulumi_kubernetes as kubernetes

crapi_identity = kubernetes.apps.v1.Deployment("crapiIdentity",
    metadata={
        "name": "crapi-identity",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "crapi-identity",
            },
        },
        "template": {
            "metadata": {
                "labels": {
                    "app": "crapi-identity",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "crapi-identity-configmap",
                        },
                    }],
                    "image": "crapi/crapi-identity:latest",
                    "image_pull_policy": "Always",
                    "name": "crapi-identity",
                    "ports": [{
                        "container_port": 8080,
                    }],
                    "readiness_probe": {
                        "initial_delay_seconds": 15,
                        "period_seconds": 10,
                        "tcp_socket": {
                            "port": 8080,
                        },
                    },
                    "resources": {
                        "limits": {
                            "cpu": "500m",
                        },
                        "requests": {
                            "cpu": "256m",
                        },
                    },
                    "volume_mounts": [{
                        "mount_path": "/.keys",
                        "name": "jwt-key-secret",
                        "read_only": True,
                    }],
                }],
                "init_containers": [{
                    "args": [
                        "service",
                        "postgresdb",
                    ],
                    "image": "groundnuty/k8s-wait-for:v1.3",
                    "image_pull_policy": "Always",
                    "name": "wait-for-postgres",
                }],
                "volumes": [{
                    "name": "jwt-key-secret",
                    "secret": {
                        "secret_name": "jwt-key-secret",
                    },
                }],
            },
        },
    })
crapi_identity_configmap = kubernetes.core.v1.ConfigMap("crapiIdentityConfigmap",
    data={
        "APP_NAME": "crapi-identity",
        "DB_DRIVER": "postgresql",
        "DB_HOST": "postgresdb",
        "DB_NAME": "crapi",
        "DB_PASSWORD": "crapisecretpassword",
        "DB_PORT": "5432",
        "DB_USER": "admin",
        "ENABLE_LOG4J": "true",
        "ENABLE_SHELL_INJECTION": "false",
        "JWT_EXPIRATION": "604800000",
        "JWT_SECRET": "crapi",
        "MAILHOG_DOMAIN": "example.com",
        "MAILHOG_HOST": "mailhog",
        "MAILHOG_PORT": "1025",
        "SERVER_PORT": "8080",
        "SMTP_AUTH": "true",
        "SMTP_EMAIL": "user@example.com",
        "SMTP_FROM": "no-reply@example.com",
        "SMTP_HOST": "smtp.example.com",
        "SMTP_PASS": "xxxxxxxxxxxxxx",
        "SMTP_PORT": "587",
        "SMTP_STARTTLS": "true",
    },
    metadata={
        "labels": {
            "app": "crapi-identity",
        },
        "name": "crapi-identity-configmap",
    })
crapi_identity1 = kubernetes.core.v1.Service("crapiIdentity1",
    metadata={
        "labels": {
            "app": "crapi-identity",
        },
        "name": "crapi-identity",
    },
    spec={
        "ports": [{
            "name": "java",
            "port": 8080,
        }],
        "selector": {
            "app": "crapi-identity",
        },
    })
