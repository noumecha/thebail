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

    def to_representation(self, instance):
        """Personnaliser la représentation pour l'affichage"""
        pays = Pays.objects.get(id=instance.pays_id).LibelleFR if instance.pays_id else None,
        region = Regions.objects.get(id=instance.region_id).Libelle if instance.region_id else None,
        departement = Departements.objects.get(id=instance.departement_id).LibelleFR if instance.departement_id else None,
        arrondissement = Arrondissemements.objects.get(id=instance.arrondissement_id).LibelleFR if instance.arrondissement_id else None,
        representation = {
            'id': instance.id,
            'Designation': instance.Designation,
            'type_construction_id': instance.Construction_id,
            'type_location_id': instance.Type_location_id,
            'Date_Construction': instance.Date_Construction,
            'Nombre_de_pieces': str(instance.Nombre_de_pieces) if instance.Nombre_de_pieces else None,
            'Superficie_louer': str(instance.Superficie_louer) if instance.Superficie_louer else None,
            'statut_batisse_id': instance.Situation_batisse_id,
            'revetement_int_id': instance.Revetement_interieure_id,
            'revetement_ext_id': instance.Revetement_exterieure_id,
            'observation': instance.observation,
            'pays_id': instance.pays_id,
            'pays': {
                'id': instance.pays_id,
                'libelle': pays
            },
            'ville': instance.Ville,
            'rue': instance.Rue,
            'region_id': instance.region_id,
            'region': {
                'id': instance.region_id,
                'libelle': region
            },
            'departement_id': instance.departement_id,
            'departement': {
                'id': instance.departement_id,
                'libelle': departement
            },
            'arrondissement_id': instance.arrondissement_id,
            'arrondissement': {
                'id': instance.arrondissement_id,
                'libelle': arrondissement
            },
            'quartier': instance.Quartier,
            'coordonnees_gps': instance.Coordonee_gps,
            'elements_description': [],
            'occupants_residents': [],
            'occupants_bureaux': []
        }
        # Éléments de description
        elements = ImmeubleElement.objects.filter(immeuble=instance)
        representation['elements_description'] = [
            {
                'element_id': el.element_id,
                'statut': el.statut,
                'nombre': el.nombre
            }
            for el in elements
        ]
        # Occupants résidents
        occupants_res = Occupants.objects.filter(Immeuble=instance)
        representation['occupants_residents'] = [
            {
                'nom_prenom': occ.Nom_Prenom_occupant_residence,
                'administration': occ.Administration_rattachement.id if occ.Administration_rattachement else None,
                'administration_rattachement': {
                    'id': occ.Administration_rattachement.id if occ.Administration_rattachement else None,
                    'libelle': occ.Administration_rattachement.LibelleFr if occ.Administration_rattachement else None
                },
                'fonction': occ.Fonction_occupant_residence,
                'matricule': occ.Matricule_occupant_residence,
                'ref_acte': occ.Ref_ActeJuridique_attribution,
                'date_signature': occ.Date_Signature_acte_juridique
            }
            for occ in occupants_res
        ]
        # Occupants bureaux
        occupants_bur = OccupantBureaux.objects.filter(Immeuble=instance)
        representation['occupants_bureaux'] = [
            {
                'service': occ.Service_occupant_bureau.id if occ.Service_occupant_bureau else None,
                'service_occupant_bureau' : {
                    'id': occ.Service_occupant_bureau.id if occ.Service_occupant_bureau else None,
                    'libelle': occ.Service_occupant_bureau.LibelleFr if occ.Service_occupant_bureau else None
                },
                'administration': occ.Administration_correspondante.id if occ.Administration_correspondante else None,
                'administration_correspondante': {
                    'id': occ.Administration_correspondante.id if occ.Administration_correspondante else None,
                    'libelle': occ.Administration_correspondante.LibelleFr if occ.Administration_correspondante else None
                },
                'fonction_responsable': occ.Fonction_occupant_bureau,
                'ref_acte': occ.Ref_ActeJuridique_attribution,
                'date_signature': occ.Date_signature_acte_attribution
            }
            for occ in occupants_bur
        ]

        return representation
