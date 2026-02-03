from rest_framework import serializers
from ..models import *

class AvenantSerializer(serializers.ModelSerializer):
    ancien_bailleur_id = serializers.IntegerField(required=False, allow_null=True)
    nouveau_bailleur_id = serializers.IntegerField(required=False, allow_null=True)
    reference = serializers.CharField(source='Ref_Avenant', required=False, allow_null=True)
    date_signature = serializers.CharField(source="Date_Signature", required=False, allow_null=True)
    date_effet = serializers.CharField(source="Date_effet", required=False, allow_null=True)
    ancien_loyer_mensuel = serializers.DecimalField(source="Montant_TTC_Mensuel_ancien", required=False, allow_null=True, max_digits=14, decimal_places=0)
    nouveau_loyer_mensuel = serializers.DecimalField(source="Montant_TTC_Mensuel_Nouveau", required=False, allow_null=True, max_digits=14, decimal_places=0)

    class Meta:
        model = Avenants
        fields = '__all__'
