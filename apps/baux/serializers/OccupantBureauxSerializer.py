from rest_framework import serializers
from ..models import *

class OccupantBureauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupantBureaux
        fields = '__all__'
