from rest_framework import serializers
from ..models import *

class AyantDroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayant_droits
        fields = '__all__'
        # ✅ Désactiver la validation unique si nécessaire
        extra_kwargs = {
            'Nom_Prenom_ayant_droit': {'validators': []},
        }
