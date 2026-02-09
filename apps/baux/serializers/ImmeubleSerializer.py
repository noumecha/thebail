from rest_framework import serializers
from ..models import *
from .ElementDescriptionLinkSerializer import ElementDescriptionLinkSerializer
from .OccupantBureauxSerializer import OccupantBureauxSerializer
from .OccupantResidentSerializer import OccupantResidentSerializer

class ImmeubleSerializer(serializers.ModelSerializer):
    # ✅ Champs imbriqués
    elements_description = ElementDescriptionLinkSerializer(many=True, write_only=True, required=False)
    occupants_residents = OccupantResidentSerializer(many=True, required=False, write_only=True)
    occupants_bureaux = OccupantBureauxSerializer(many=True, required=False, write_only=True)

    # ✅ Mapper les noms frontend vers les noms du modèle Django - pour le FK
    type_construction_id = serializers.IntegerField(source='Construction_id', required=False, allow_null=True)
    type_location_id = serializers.IntegerField(source='Type_location_id', required=False, allow_null=True)
    statut_batisse_id = serializers.IntegerField(source='Situation_batisse_id', required=False, allow_null=True)
    revetement_int_id = serializers.IntegerField(source='Revetement_interieure_id', required=False, allow_null=True)
    revetement_ext_id = serializers.IntegerField(source='Revetement_exterieure_id', required=False, allow_null=True)

    class Meta:
        model = Immeubles
        fields = '__all__'
        # ✅ Désactiver la validation unique pour permettre l'update
        extra_kwargs = {
            'Designation': {'validators': []},
        }

    def validate_Designation(self, value):
        """Validation manuelle de Designation"""
        # En mode update, si la valeur n'a pas changé, pas de validation
        if self.instance and self.instance.Designation == value:
            return value

        # Sinon, vérifier l'unicité
        if Immeubles.objects.filter(Designation=value).exists():
            raise serializers.ValidationError("Un immeuble avec cette désignation existe déjà.")

        return value

    def create(self, validated_data):
        """Créer l'immeuble avec toutes ses relations"""
        # ✅ Extraire les données imbriquées
        elements_data = validated_data.pop('elements_description', [])
        occupants_residents_data = validated_data.pop('occupants_residents', [])
        occupants_bureaux_data = validated_data.pop('occupants_bureaux', [])

        # ✅ Créer l'immeuble
        immeuble = Immeubles.objects.create(**validated_data)

        # ✅ Créer les liens avec les éléments de description
        for element_data in elements_data:
            ImmeubleElement.objects.create(
                immeuble=immeuble,
                element_id=element_data['element_id'],
                statut=element_data['statut'],
                nombre=element_data['nombre']
            )

        # ✅ Créer les occupants résidents
        for occupant_data in occupants_residents_data:
            Occupants.objects.create(
                Immeuble=immeuble,
                **occupant_data
            )

        # ✅ Créer les occupants bureaux
        for occupant_data in occupants_bureaux_data:
            OccupantBureaux.objects.create(
                Immeuble=immeuble,
                **occupant_data
            )

        return immeuble

    def update(self, instance, validated_data):
        """Mettre à jour un immeuble"""
        elements_data = validated_data.pop('elements_description', None)
        occupants_residents_data = validated_data.pop('occupants_residents', None)
        occupants_bureaux_data = validated_data.pop('occupants_bureaux', None)

        # Mettre à jour les champs simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour les éléments
        if elements_data is not None:
            existing_element_ids = []
            for element_data in elements_data:
                ImmeubleElement.objects.update_or_create(
                    immeuble=instance,
                    element_id=element_data['element_id'],
                    defaults={
                        'statut': element_data['statut'],
                        'nombre': element_data['nombre']
                    }
                )
                existing_element_ids.append(element_data['element_id'])

            ImmeubleElement.objects.filter(
                immeuble=instance
            ).exclude(
                element_id__in=existing_element_ids
            ).delete()

        # ✅ Supprimer et recréer les occupants résidents (évite les problèmes d'unicité)
        if occupants_residents_data is not None:
            Occupants.objects.filter(Immeuble=instance).delete()
            for occupant_data in occupants_residents_data:
                Occupants.objects.create(
                    Immeuble=instance,
                    **occupant_data
                )

        # ✅ Supprimer et recréer les occupants bureaux
        if occupants_bureaux_data is not None:
            OccupantBureaux.objects.filter(Immeuble=instance).delete()
            for occupant_data in occupants_bureaux_data:
                OccupantBureaux.objects.create(
                    Immeuble=instance,
                    **occupant_data
                )

        return instance
