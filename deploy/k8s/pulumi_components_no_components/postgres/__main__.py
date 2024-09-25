import pulumi
import pulumi_kubernetes as kubernetes

postgres_config = kubernetes.core.v1.ConfigMap("postgresConfig",
    data={
        "POSTGRES_DB": "crapi",
        "POSTGRES_PASSWORD": "crapisecretpassword",
        "POSTGRES_USER": "admin",
    },
    metadata={
        "labels": {
            "app": "postgresdb",
        },
        "name": "postgres-config",
    })
postgresdb = kubernetes.core.v1.Service("postgresdb",
    metadata={
        "labels": {
            "app": "postgresdb",
        },
        "name": "postgresdb",
    },
    spec={
        "ports": [{
            "name": "postgres",
            "port": 5432,
        }],
        "selector": {
            "app": "postgresdb",
        },
    })
postgres_pv_claim = kubernetes.core.v1.PersistentVolumeClaim("postgresPvClaim",
    metadata={
        "labels": {
            "app": "postgresdb",
        },
        "name": "postgres-pv-claim",
    },
    spec={
        "access_modes": ["ReadWriteOnce"],
        "resources": {
            "requests": {
                "storage": "1000Mi",
            },
        },
    })
postgresdb1 = kubernetes.apps.v1.StatefulSet("postgresdb1",
    metadata={
        "name": "postgresdb",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "postgresdb",
            },
        },
        "service_name": "postgresdb",
        "template": {
            "metadata": {
                "labels": {
                    "app": "postgresdb",
                },
            },
            "spec": {
                "containers": [{
                    "args": [
                        "-c",
                        "max_connections=500",
                    ],
                    "env_from": [{
                        "config_map_ref": {
                            "name": "postgres-config",
                        },
                    }],
                    "image": "postgres:14",
                    "image_pull_policy": "IfNotPresent",
                    "name": "postgres",
                    "ports": [{
                        "container_port": 5432,
                    }],
                    "volume_mounts": [{
                        "mount_path": "/var/lib/postgresql/data",
                        "name": "postgres-data",
                        "sub_path": "postgres",
                    }],
                }],
                "volumes": [{
                    "name": "postgres-data",
                    "persistent_volume_claim": {
                        "claim_name": "postgres-pv-claim",
                    },
                }],
            },
        },
    })
