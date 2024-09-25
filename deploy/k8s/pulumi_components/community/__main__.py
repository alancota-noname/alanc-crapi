import pulumi
from crapiCommunity import CrapiCommunity
from crapiCommunity1 import CrapiCommunity1
from crapiCommunityConfigmap import CrapiCommunityConfigmap

crapi_community = CrapiCommunity("crapiCommunity")
crapi_community_configmap = CrapiCommunityConfigmap("crapiCommunityConfigmap")
crapi_community1 = CrapiCommunity1("crapiCommunity1")
