from rest_framework import serializers
from ..models import *
from .LocalisationSerializer import LocalisationSerializer
from .ElementDescriptionLinkSerializer import ElementDescriptionLinkSerializer
from .OccupantBureauxSerializer import OccupantBureauxSerializer
from .OccupantResidentSerializer import OccupantResidentSerializer

class ImmeubleSerializer(serializers.ModelSerializer):
    # ✅ Champs imbriqués
    localisation = LocalisationSerializer(write_only=True)
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
        localisation_data = validated_data.pop('localisation', {})
        elements_data = validated_data.pop('elements_description', [])
        occupants_residents_data = validated_data.pop('occupants_residents', [])
        occupants_bureaux_data = validated_data.pop('occupants_bureaux', [])

        # ✅ Ajouter les données de localisation directement dans l'immeuble
        if localisation_data:
            validated_data['pays_id'] = localisation_data.get('pays_id')
            validated_data['Ville'] = localisation_data.get('ville')
            validated_data['Rue'] = localisation_data.get('rue')
            validated_data['region_id'] = localisation_data.get('region_id')
            validated_data['departement_id'] = localisation_data.get('departement_id')
            validated_data['arrondissement_id'] = localisation_data.get('arrondissement_id')
            validated_data['Quartier'] = localisation_data.get('quartier')
            validated_data['Coordonee_gps'] = localisation_data.get('coordonnees_gps')

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
        localisation_data = validated_data.pop('localisation', None)
        elements_data = validated_data.pop('elements_description', None)
        occupants_residents_data = validated_data.pop('occupants_residents', None)
        occupants_bureaux_data = validated_data.pop('occupants_bureaux', None)
        # Mettre à jour les champs simples
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Mettre à jour la localisation
        if localisation_data:
            for attr, value in localisation_data.items():
                setattr(instance, attr, value)
            instance.save()

        # Mettre à jour les éléments de description
        if elements_data is not None:
            # Supprimer les anciens liens
            ImmeubleElement.objects.filter(immeuble=instance).delete()
            # Créer les nouveaux
            for element_data in elements_data:
                ImmeubleElement.objects.create(
                    immeuble=instance,
                    element_id=element_data['element_id'],
                    statut=element_data['statut'],
                    nombre=element_data['nombre']
                )

        # Mettre à jour les occupants résidents
        if occupants_residents_data is not None:
            Occupants.objects.filter(immeuble=instance).delete()
            for occupant_data in occupants_residents_data:
                Occupants.objects.create(
                    immeuble=instance,
                    **occupant_data
                )

        # Mettre à jour les occupants bureaux
        if occupants_bureaux_data is not None:
            OccupantBureaux.objects.filter(immeuble=instance).delete()
            for occupant_data in occupants_bureaux_data:
                OccupantBureaux.objects.create(
                    immeuble=instance,
                    **occupant_data
                )

        return instance
