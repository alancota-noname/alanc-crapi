import pulumi
from gatewayService import GatewayService
from gatewayService1 import GatewayService1
from gatewayServiceConfigmap import GatewayServiceConfigmap

gateway_service = GatewayService("gatewayService")
gateway_service_configmap = GatewayServiceConfigmap("gatewayServiceConfigmap")
gateway_service1 = GatewayService1("gatewayService1")
