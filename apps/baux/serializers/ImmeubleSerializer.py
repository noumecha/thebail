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

        # ✅ Mettre à jour les éléments (update_or_create au lieu de delete)
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

            # Supprimer uniquement ceux qui ne sont plus présents
            ImmeubleElement.objects.filter(
                immeuble=instance
            ).exclude(
                element_id__in=existing_element_ids
            ).delete()

        # ✅ Mettre à jour les occupants résidents (update_or_create)
        if occupants_residents_data is not None:
            existing_occupant_ids = []
            for occupant_data in occupants_residents_data:
                nom_prenom = occupant_data.get('Nom_Prenom_occupant_residence')
                occupant, created = Occupants.objects.update_or_create(
                    Immeuble=instance,
                    Nom_Prenom_occupant_residence=nom_prenom,
                    defaults=occupant_data
                )
                existing_occupant_ids.append(occupant.id)

            # Supprimer ceux qui ne sont plus présents
            Occupants.objects.filter(
                Immeuble=instance
            ).exclude(
                id__in=existing_occupant_ids
            ).delete()

        # ✅ Mettre à jour les occupants bureaux (update_or_create)
        if occupants_bureaux_data is not None:
            # Supprimer et recréer (car pas de champ unique évident)
            OccupantBureaux.objects.filter(Immeuble=instance).delete()
            for occupant_data in occupants_bureaux_data:
                OccupantBureaux.objects.create(
                    Immeuble=instance,
                    **occupant_data
                )

        return instance
