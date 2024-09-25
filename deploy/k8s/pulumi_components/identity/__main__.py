import pulumi
from crapiIdentity import CrapiIdentity
from crapiIdentity1 import CrapiIdentity1
from crapiIdentityConfigmap import CrapiIdentityConfigmap

crapi_identity = CrapiIdentity("crapiIdentity")
crapi_identity_configmap = CrapiIdentityConfigmap("crapiIdentityConfigmap")
crapi_identity1 = CrapiIdentity1("crapiIdentity1")
