from rest_framework import serializers
from ..models import *

class OccupantResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupants
        fields = '__all__'
