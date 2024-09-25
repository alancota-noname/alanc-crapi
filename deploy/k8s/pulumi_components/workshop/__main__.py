import pulumi
from crapiWorkshop import CrapiWorkshop
from crapiWorkshop1 import CrapiWorkshop1
from crapiWorkshopConfigmap import CrapiWorkshopConfigmap

crapi_workshop = CrapiWorkshop("crapiWorkshop")
crapi_workshop_configmap = CrapiWorkshopConfigmap("crapiWorkshopConfigmap")
crapi_workshop1 = CrapiWorkshop1("crapiWorkshop1")
