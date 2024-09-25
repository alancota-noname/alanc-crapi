import pulumi
import pulumi_kubernetes as kubernetes

mailhog = kubernetes.apps.v1.Deployment("mailhog",
    metadata={
        "name": "mailhog",
        "namespace": "crapi",
    },
    spec={
        "min_ready_seconds": 10,
        "progress_deadline_seconds": 600,
        "replicas": 1,
        "selector": {
            "match_labels": {
                "app": "mailhog",
            },
        },
        "template": {
            "metadata": {
                "annotations": {
                    "sidecar_traceable_ai_inject": "false",
                },
                "labels": {
                    "app": "mailhog",
                },
            },
            "spec": {
                "containers": [{
                    "env_from": [{
                        "config_map_ref": {
                            "name": "mailhog-configmap",
                        },
                    }],
                    "image": "crapi/mailhog:latest",
                    "image_pull_policy": "Always",
                    "liveness_probe": {
                        "initial_delay_seconds": 15,
                        "period_seconds": 60,
                        "tcp_socket": {
                            "port": 1025,
                        },
                    },
                    "name": "mailhog",
                    "ports": [
                        {
                            "container_port": 8025,
                            "name": "web",
                            "protocol": "TCP",
                        },
                        {
                            "container_port": 1025,
                            "name": "smtp",
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
                    "resources": {
                        "limits": {
                            "cpu": "1",
                            "memory": "1024Mi",
                        },
                        "requests": {
                            "cpu": "50m",
                            "memory": "64Mi",
                        },
                    },
                }],
                "security_context": {
                    "run_as_group": 0,
                    "run_as_user": 0,
                },
            },
        },
    })
mailhog_web = kubernetes.core.v1.Service("mailhogWeb",
    metadata={
        "name": "mailhog-web",
        "namespace": "crapi",
    },
    spec={
        "ports": [{
            "name": "web",
            "node_port": 30025,
            "port": 8025,
            "protocol": "TCP",
        }],
        "selector": {
            "app": "mailhog",
        },
        "session_affinity": "None",
        "type": kubernetes.core.v1.ServiceSpecType.LOAD_BALANCER,
    })
mailhog_configmap = kubernetes.core.v1.ConfigMap("mailhogConfigmap",
    data={
        "MH_MONGO_URI": "admin:crapisecretpassword@mongodb:27017",
        "MH_STORAGE": "mongodb",
    },
    metadata={
        "labels": {
            "app": "mailhog",
        },
        "name": "mailhog-configmap",
    })
mailhogcrapi = kubernetes.core.v1.Service("mailhogcrapi",
    metadata={
        "name": "mailhog",
        "namespace": "crapi",
    },
    spec={
        "ports": [{
            "name": "smtp",
            "port": 1025,
            "protocol": "TCP",
            "target_port": 1025,
        }],
        "selector": {
            "app": "mailhog",
        },
        "session_affinity": "None",
        "type": kubernetes.core.v1.ServiceSpecType.CLUSTER_IP,
    })
