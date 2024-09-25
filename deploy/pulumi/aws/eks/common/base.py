from pulumi_kubernetes.meta.v1 import ObjectMetaArgs
from config import settings


class MetadataBase(ObjectMetaArgs):
    def __init__(
        self,
        labels: dict[str, str] | None = None,
        annotations: dict[str, str] | None = None,
        name: str | None = None,
        namespace: str | None = settings.app_namespace,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.labels = labels or {}
        self.annotations = annotations or {}
        self.name = name
        self.namespace = namespace
        self.kwargs = kwargs

        for key, value in kwargs.items():
            setattr(self, key, value)
