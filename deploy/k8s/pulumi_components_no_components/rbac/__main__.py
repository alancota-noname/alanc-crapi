import pulumi
import pulumi_kubernetes as kubernetes

waitfor_reader = kubernetes.rbac.v1.ClusterRole("waitforReader",
    metadata={
        "name": "waitfor-reader",
        "namespace": "crapi",
    },
    rules=[{
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
    }])
waitfor_grant = kubernetes.rbac.v1.ClusterRoleBinding("waitforGrant",
    metadata={
        "name": "waitfor-grant",
        "namespace": "crapi",
    },
    role_ref={
        "api_group": "",
        "kind": "ClusterRole",
        "name": "waitfor-reader",
    },
    subjects=[{
        "api_group": "",
        "kind": "ServiceAccount",
        "name": "default",
        "namespace": "crapi",
    }])
