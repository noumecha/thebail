from rest_framework import serializers
from ..models import *

class NonMandatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Non_Mandatement
        fields = '__all__'
