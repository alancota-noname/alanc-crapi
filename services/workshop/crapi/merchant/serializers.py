#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""
contains serializers for Merchant APIs
"""
from rest_framework import serializers
from crapi.mechanic.models import Mechanic, ServiceRequest
from crapi.mechanic.serializers import VehicleSerializer


class ContactMechanicSerializer(serializers.Serializer):
    """
    Serializer for Contact Mechanic model.
    """

    mechanic_api = serializers.CharField()
    repeat_request_if_failed = serializers.BooleanField(required=False)
    number_of_repeats = serializers.IntegerField(required=False)


class MechanicPublicSerializer(serializers.ModelSerializer):
    """
    Serializer for Mechanic model
    """

    class Meta:
        """
        Meta class for MechanicPublicSerializer
        """

        model = Mechanic
        fields = ("id", "mechanic_code")


class UserServiceRequestSerializer(serializers.ModelSerializer):
    """
    Serializer for Mechanic model
    """

    mechanic = MechanicPublicSerializer()
    vehicle = VehicleSerializer()
    created_on = serializers.DateTimeField(format="%d %B, %Y, %H:%M:%S")

    class Meta:
        """
        Meta class for UserServiceRequestSerializer
        """

        model = ServiceRequest
        fields = (
            "id",
            "mechanic",
            "vehicle",
            "problem_details",
            "status",
            "created_on",
        )
