import base64
from pathlib import Path
from config import settings


def encode_file(file_path):
    # Read the contents of the jwks.json file
    with open(file_path, "rb") as file:
        file_content = file.read()
    # Base64 encode the file content
    encoded_content = base64.b64encode(file_content).decode("utf-8")
    return encoded_content


def list_folders(directory):
    return [item.name for item in Path(directory).iterdir() if item.is_dir()]


def k8s_labels(
    name: str,
    component: str,
    project_version: str = settings.project_version,
    project_prefix: str = settings.project_prefix,
    managed_by: str = "Pulumi",
    instance: str | None = None,
    **kwargs,  # Additional labels to add to the metadata object
) -> dict[str, str]:
    if not instance:
        instance = f"{project_prefix}-{settings.app_name}-{settings.project_unique_id}"

    labels = {
        # Kubernetes shared labels
        "app": name,
        "app.kubernetes.io/name": name,
        "app.kubernetes.io/instance": instance,
        "app.kubernetes.io/version": project_version,
        "app.kubernetes.io/component": component,
        "app.kubernetes.io/part-of": settings.app_name,
        "app.kubernetes.io/managed-by": managed_by,
    }

    # Merge any additional labels from kwargs
    labels.update(kwargs)

    return labels


# Deploy the crAPI App to the EKS Cluster
