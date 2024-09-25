"""An AWS Python Pulumi program"""

import pulumi
import pulumi_aws as aws
import pulumi_awsx as awsx
import pulumi_eks as eks
from pulumi_eks import AuthenticationMode as eks_auth_mode
import pulumi_kubernetes as kubernetes

# Get some values from the Pulumi configuration (or use defaults)
config = pulumi.Config()
project_prefix = config.require("projectPrefix")
project_owner = config.get("projectOwnerTag")
vpc_network_cidr = config.get("vpcNetworkCidr", "10.60.0.0/16")
vpc_name = config.get("vpcName", "alanc-crapi-vpc")
vpc_num_zones = config.get_int("vpcNumberAvailabilityZones", 2)
create_security_group = config.get_bool("createSecurityGroup", False)
allow_all_from = config.get("securityGroupIngressAllowAllFrom", "0.0.0.0/0")

# EKS Cluster Configuration
create_eks_cluster = config.get_bool("createAwsEksCluster", False)
cluster_name = config.get("awsEksClusterName", "alanc-crapi-cluster")
min_cluster_size = config.get_int("minClusterSize", 2)
max_cluster_size = config.get_int("maxClusterSize", 3)
desired_cluster_size = config.get_int("desiredClusterSize", 2)
eks_node_instance_type = config.get("eksNodeInstanceType", "t2.small")

print(f"AWS Region: {aws.get_region().name}")

# Create the AWS VPC
vpc = awsx.ec2.Vpc(
	vpc_name,
	enable_dns_hostnames=True,
	cidr_block=vpc_network_cidr,
	number_of_availability_zones=vpc_num_zones,
	subnet_specs=[
		awsx.ec2.SubnetSpecArgs(
			type=awsx.ec2.SubnetType.PUBLIC,
			cidr_mask=24,
		),
		awsx.ec2.SubnetSpecArgs(
			type=awsx.ec2.SubnetType.PRIVATE,
			cidr_mask=24,
		),
	],
	tags={
		"Name": vpc_name,
		"Owner": project_owner,
	}
)

# Create the AWS Security Groups
security_group_allow_all = aws.ec2.SecurityGroup(
	resource_name=f"{project_prefix}-allow-all",
	description="Allow All traffic from Home Network",
	vpc_id=vpc.vpc_id,
	tags={
		"Owner": project_owner,
		"Cleanup": "false",
	})

# Create ingress and egress rules for the security group

# Allow all traffic from Home Network (0.0.0.0/0)
ingress_allow_all_ipv4 = aws.vpc.SecurityGroupIngressRule(
	resource_name="allow-all-ipv4-ingress",
	security_group_id=security_group_allow_all.id,
	cidr_ipv4=allow_all_from,
	from_port=-1,
	to_port=-1,
	ip_protocol="-1",
)

# Allow outbound traffic
egress_allow_all_ipv4 = aws.vpc.SecurityGroupIngressRule(
	resource_name="allow-all-ipv4-egress",
	security_group_id=security_group_allow_all.id,
	cidr_ipv4="0.0.0.0/0",
	ip_protocol="-1",
)


if create_eks_cluster:
	# Create the EKS cluster
	new_eks_cluster = eks.Cluster(
		# Cluster Name
		cluster_name,
		# Authentication Mode
		authentication_mode=eks_auth_mode.API_AND_CONFIG_MAP,
		# Put the cluster in the new VPC created earlier
		vpc_id=vpc.vpc_id,
		# Public subnets will be used for load balancers
		public_subnet_ids=vpc.public_subnet_ids,
		# Private subnets will be used for cluster nodes
		private_subnet_ids=vpc.private_subnet_ids,
		# Change configuration values to change any of the following settings
		instance_type=eks_node_instance_type,
		desired_capacity=desired_cluster_size,
		min_size=min_cluster_size,
		max_size=max_cluster_size,
		# Do not give worker nodes a public IP address
		node_associate_public_ip_address=False,
		# Change these values for a private cluster (VPN access required)
		endpoint_private_access=False,
		endpoint_public_access=True
	)
	pulumi.export("kubeconfig", new_eks_cluster.kubeconfig)
	pulumi.export("clusterName", new_eks_cluster.eks_cluster)
else:
	# Lookup for the existing EKS cluster
	eks_cluster = aws.eks.get_cluster(name=cluster_name)
	pulumi.export("clusterName", eks_cluster.name)
	pulumi.export("clusterCertificates", eks_cluster.certificate_authorities[0].data)


# Export values to be used in other Pulumi projects
pulumi.export("vpcId", vpc.vpc_id)
pulumi.export("vpcSubnets", vpc.subnets)
pulumi.export("publicSubnetIds", vpc.public_subnet_ids)
pulumi.export("privateSubnetIds", vpc.private_subnet_ids)

