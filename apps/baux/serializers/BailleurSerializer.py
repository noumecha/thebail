from rest_framework import serializers
from ..models import *

class BailleurSerializer(serializers.ModelSerializer):
    ayants_droit = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Bailleurs
        fields = '__all__'

    def validate(self, data):
        """Validations métier pour le bailleur"""
        type_personne = data.get('type_personne')

        # Si personne physique, NIU et CNI obligatoires
        if type_personne == 'PHYSIQUE':
            if not data.get('niu'):
                raise serializers.ValidationError({
                    'niu': 'Le NIU est obligatoire pour une personne physique'
                })
            if not data.get('cni'):
                raise serializers.ValidationError({
                    'cni': 'La CNI est obligatoire pour une personne physique'
                })

        # Si personne morale, raison sociale obligatoire
        if type_personne == 'MORALE':
            if not data.get('nom_prenom_raison_sociale'):
                raise serializers.ValidationError({
                    'nom_prenom_raison_sociale': 'La raison sociale est obligatoire'
                })

        return data
