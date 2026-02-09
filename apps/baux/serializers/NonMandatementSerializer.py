from rest_framework import serializers
from ..models import *

class NonMandatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = Non_Mandatement
        fields = '__all__'
        # ✅ Désactiver la validation unique
        extra_kwargs = {
            'Ref_Attestattion': {'validators': []},
        }
