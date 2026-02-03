from rest_framework import serializers
from ..models import *

class AyantDroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayant_droits
        fields = '__all__'
