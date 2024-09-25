import pulumi
import pulumi_kubernetes as kubernetes

mongodb_config = kubernetes.core.v1.ConfigMap("mongodbConfig",
    data={
        "MONGO_INITDB_ROOT_PASSWORD": "crapisecretpassword",
        "MONGO_INITDB_ROOT_USERNAME": "admin",
    },
    metadata={
        "labels": {
            "app": "mongodb",
        },
        "name": "mongodb-config",
    })
mongodb = kubernetes.core.v1.Service("mongodb",
    metadata={
        "labels": {
            "app": "mongodb",
        },
        "name": "mongodb",
    },
    spec={
        "ports": [{
            "name": "mongo",
            "port": 27017,
        }],
        "selector": {
            "app": "mongodb",
        },
    })
mongodb_pv_claim = kubernetes.core.v1.PersistentVolumeClaim("mongodbPvClaim",
    metadata={
        "labels": {
            "app": "mongo",
        },
        "name": "mongodb-pv-claim",
    },
    spec={
        "access_modes": ["ReadWriteOnce"],
        "resources": {
            "requests": {
                "storage": "1000Mi",
            },
        },
    })
mongodb1 = kubernetes.apps.v1.StatefulSet("mongodb1",
    metadata={
        "name": "mongodb",
    },
    spec={
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "mongodb",
            },
        },
        "service_name": "mongodb",
        "template": {
            "metadata": {
                "labels": {
                    "app": "mongodb",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "mongodb-config",
                        },
                    }],
                    "image": "mongo:4.4",
                    "image_pull_policy": "IfNotPresent",
                    "name": "mongodb",
                    "volume_mounts": [{
                        "mount_path": "/data/db",
                        "name": "mongodb-data",
                    }],
                }],
                "volumes": [{
                    "name": "mongodb-data",
                    "persistent_volume_claim": {
                        "claim_name": "mongodb-pv-claim",
                    },
                }],
            },
        },
    })
