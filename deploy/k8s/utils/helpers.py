import base64
import json
from pathlib import Path
import pulumi_docker_build as docker_build


def encode_file(file_path):
	# Read the contents of the jwks.json file
	with open(file_path, 'rb') as file:
		file_content = file.read()
	# Base64 encode the file content
	encoded_content = base64.b64encode(file_content).decode('utf-8')
	return encoded_content


def list_folders(directory):
	return [item.name for item in Path(directory).iterdir() if item.is_dir()]


def build_image(labels, auth_token, service_name, image_name, services_path, ecr_repository, docker_tag, push_to_ecr=True):
	print(f"Building image {ecr_repository.url} - {service_name}:{docker_tag}...")
	image = docker_build.Image(
		image_name,
		context={
			"location": f"{services_path}/{service_name}",
		},
		push=push_to_ecr,
		registries=[{
			"address": ecr_repository.url,
			"password": auth_token.password,
			"username": auth_token.user_name,
		}],
	# Build a multi-platform image manifest for ARM and AMD.
		platforms=[
			docker_build.Platform.LINUX_AMD64,
			docker_build.Platform.LINUX_ARM64,
		],
		labels=labels,
		tags=[
			ecr_repository.url.apply(lambda repository_url: f"{repository_url}:{docker_tag}"),
			ecr_repository.url.apply(lambda repository_url: f"{repository_url}:latest")
		]
	)

	return image

# Deploy the crAPI App to the EKS Cluster
