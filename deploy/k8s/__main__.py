import pulumi
import pulumi_awsx as awsx
import pulumi_aws as aws
import pulumi_kubernetes as k8s
from utils.helpers import list_folders, build_image, encode_file

# Get some values from the Pulumi configuration (or use defaults)
config = pulumi.Config()
project_prefix = config.require("projectPrefix")
project_owner_name = config.require("projectOwnerName")
project_owner_email = config.require("projectOwnerEmail")
project_version = config.require("projectVersion")
project_repository = config.require("projectRepository")
project_description = config.get("projectDescription")

# Pulumi Information
pulumi_owner_tag = config.get("pulumiProjectOwnerTag")
pulumi_organization = config.get("pulumiOrganizationName")
pulumi_infra_project = config.get("pulumiProjectName")
pulumi_infra_stack = config.get("pulumiStackName")

app_name = config.get("appName")
services_path = config.get("servicesPath")
docker_tag = config.get("dockerTag", "latest")
push_to_ecr = config.get_bool("pushToEcr", True)
build_images = config.get_bool("buildCustomImages", True)
services_to_build = config.get("servicesToBuild", "all")

# Kubernetes Configuration
crapi_k8s_namespace = config.get("eksAppNamespace", "alanc-crapi")
crapi_k8s_jwt_key_name = config.get("crapiJWTKeySecretKeyName")
crapi_k8s_jwt_key_file = config.get("crapiJWTKeySecretKeyFile")

# Build all the images under ../../services

# Grab a list of all folders in the services directory
folders = list_folders(services_path)

# Loop through each folder and build the image
images = {}
for folder in folders:
	if build_images:
		# Build only services in the list
		if folder in services_to_build or services_to_build == "all":
			# Create ECR Repository for each application
			ecr_repository = awsx.ecr.Repository(
				f"{app_name}-{folder}",
				awsx.ecr.RepositoryArgs(force_delete=True),
			)
			# Fetch the credentials to use the ECR
			auth_token = aws.ecr.get_authorization_token_output()

			# Image labels
			labels = {
				"com.nonamesec.sa.project.name": app_name,
				"com.nonamesec.sa.project.version": project_version,
				"com.nonamesec.sa.project.repository": project_repository,
				"com.nonamesec.sa.project.description": project_description,
				"com.nonamesec.sa.project.owner.name": project_owner_name,
				"com.nonamesec.sa.project.owner.email": project_owner_email,
				"com.nonamesec.sa.project.prefix": project_prefix,
				"com.nonamesec.sa.project.service": folder,
				"com.nonamesec.sa.project.pulumi.tag": pulumi_owner_tag,
				"com.nonamesec.sa.project.pulumi.org": pulumi.get_organization(),
				"com.nonamesec.sa.project.pulumi.project": pulumi.get_project(),
				"com.nonamesec.sa.project.pulumi.stack": pulumi.get_stack(),
			}

			image = build_image(
				auth_token=auth_token,
				service_name=folder,
				image_name=f"{app_name}-{folder}",
				services_path=services_path,
				ecr_repository=ecr_repository,
				docker_tag=docker_tag,
				labels=labels,
				push_to_ecr=push_to_ecr
			)
			images[folder] = {
				"repo": ecr_repository.url,
				"ref": image.ref,
				"name": f"{app_name}-{folder}",
				"tag": docker_tag,
				"push": push_to_ecr
			}

# crAPI Deployments

# 1 - Create the Namespace
# namespace = k8s.core.v1.Namespace(
# 	resource_name=crapi_k8s_namespace,
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name=crapi_k8s_namespace
# 	)
# )

# # 2 - Create the JWT Key Secret
# jwt_key = k8s.core.v1.Secret(
# 	resource_name=crapi_k8s_jwt_key_name,
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name=crapi_k8s_jwt_key_name,
# 		namespace=crapi_k8s_namespace
# 	),
# 	string_data={
# 		"jwks.json": encode_file(crapi_k8s_jwt_key_file)
# 	}
# )

# # 3 - MongoDB
# k8s.core.v1.ConfigMap(
# 	resource_name="mongodb-config",
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name="mongodb-config",
# 		namespace=crapi_k8s_namespace,
# 		labels={
# 			"app": "mongodb"
# 		},
# 	),
# 	data={
# 		"MONGO_INITDB_ROOT_USERNAME": "admin",
# 		"MONGO_INITDB_ROOT_PASSWORD": "crapisecretpassword"
# 	}
# )

# mongo_pvc = k8s.core.v1.PersistentVolumeClaim(
# 	resource_name="mongodb-pvc",
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name="mongodb-pv-claim",
# 		namespace=crapi_k8s_namespace
# 	),
# 	spec=k8s.storage.v1.PersistentVolumeClaimSpecArgs(
# 		access_modes=["ReadWriteOnce"],
# 		resources=k8s.core.v1.ResourceRequirementsArgs(
# 			requests={
# 				"storage": "1Gi"
# 			}
# 		)
# 	)
# )

# k8s.apps.v1.StatefulSet(
# 	resource_name="mongodb",
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name="mongodb",
# 		namespace=crapi_k8s_namespace,
# 		labels={
# 			"app": "mongodb"
# 		},
# 	),
# 	spec=k8s.apps.v1.StatefulSetSpecArgs(
# 		replicas=1,
# 		selector=k8s.meta.v1.LabelSelectorArgs(
# 			match_labels={
# 				"app": "mongodb"
# 			}
# 		),
# 		template=k8s.core.v1.PodTemplateSpecArgs(
# 			metadata=k8s.meta.v1.ObjectMetaArgs(
# 				labels={
# 					"app": "mongodb"
# 				}
# 			),
# 			spec=k8s.core.v1.PodSpecArgs(
# 				containers=[
# 					k8s.core.v1.ContainerArgs(
# 						name="mongodb",
# 						image="mongo:4.4",
# 						env=[
# 							k8s.core.v1.EnvVarArgs(
# 								name="MONGO_INITDB_ROOT_USERNAME",
# 								value_from=k8s.core.v1.EnvVarSourceArgs(
# 									secret_key_ref=k8s.core.v1.SecretKeySelectorArgs(
# 										name="mongodb-config",
# 										key="MONGO_INITDB_ROOT_USERNAME"
# 									)
# 								)
# 							),
# 							k8s.core.v1.EnvVarArgs(
# 								name="MONGO_INITDB_ROOT_PASSWORD",
# 								value_from=k8s.core.v1.EnvVarSourceArgs(
# 									secret_key_ref=k8s.core.v1.SecretKeySelectorArgs(
# 										name="mongodb-config",
# 										key="MONGO_INITDB_ROOT_PASSWORD"
# 									)
# 								)
# 							)
# 						],
# 						ports=[
# 							k8s.core.v1.ContainerPortArgs(
# 								container_port=27017
# 							)
# 						]
# 					)
# 				],
# 				volumes=[
# 					k8s.core.v1.VolumeArgs(
# 						name="mongodb-data",
# 						persistent_volume_claim=mongo_pvc.metadata.get().name,
# 					)
# 				]
# 			)
# 		)
# 	)
# )

# k8s.core.v1.Service(
# 	resource_name="mongodb",
# 	metadata=k8s.meta.v1.ObjectMetaArgs(
# 		name="mongodb",
# 		namespace=crapi_k8s_namespace
# 	),
# 	spec=k8s.core.v1.ServiceSpecArgs(
# 		selector={
# 			"app": "mongodb"
# 		},
# 		ports=[
# 			k8s.core.v1.ServicePortArgs(
# 				port=27017,
# 				target_port=27017
# 			)
# 		]
# 	)
# )

# Exports
pulumi.export("crapiImages", images)
