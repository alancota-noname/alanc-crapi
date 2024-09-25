import pulumi
from crapiWeb import CrapiWeb
from crapiWeb1 import CrapiWeb1
from crapiWebConfigmap import CrapiWebConfigmap

crapi_web = CrapiWeb("crapiWeb")
crapi_web1 = CrapiWeb1("crapiWeb1")
crapi_web_configmap = CrapiWebConfigmap("crapiWebConfigmap")
