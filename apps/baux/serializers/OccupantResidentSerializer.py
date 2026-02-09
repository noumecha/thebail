from rest_framework import serializers
from ..models import *

class OccupantResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupants
        exclude = ['Immeuble']
        extra_kwargs = {
            'Nom_Prenom_occupant_residence': {'validators': []},
        }
