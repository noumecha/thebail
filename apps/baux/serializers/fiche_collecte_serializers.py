# serializers/fiche_collecte_serializers.py
from rest_framework import serializers
from ..models import *

class LocalisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'

    def validate(self, data):
        """Validations métier pour la localisation"""
        # Si pays étranger, ville et rue sont obligatoires
        if data.get('pays_id') and data['pays_id'] != 1:  # 1 = Cameroun
            if not data.get('ville'):
                raise serializers.ValidationError({
                    'ville': 'La ville est obligatoire pour un pays étranger'
                })

        # Si Cameroun, région/département/arrondissement obligatoires
        if data.get('pays_id') == 1:
            if not data.get('region_id'):
                raise serializers.ValidationError({
                    'region_id': 'La région est obligatoire'
                })

        return data

class ElementDescriptionLinkSerializer(serializers.Serializer):
    """Serializer pour la table intermédiaire Immeuble-ElementDescription"""
    element_id = serializers.IntegerField()
    statut = serializers.BooleanField()
    nombre = serializers.IntegerField(default=0)

class OccupantResidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Occupants
        fields = '__all__'

class OccupantBureauxSerializer(serializers.ModelSerializer):
    class Meta:
        model = OccupantBureaux
        fields = '__all__'

# serializers/fiche_collecte_serializers.py
class LocalisationSerializer(serializers.Serializer):
    """Serializer pour les données de localisation (pas un modèle séparé)"""
    pays_id = serializers.IntegerField(required=False, allow_null=True)
    ville = serializers.CharField(required=False, allow_blank=True)
    rue = serializers.CharField(required=False, allow_blank=True)
    region_id = serializers.IntegerField(required=False, allow_null=True)
    departement_id = serializers.IntegerField(required=False, allow_null=True)
    arrondissement_id = serializers.IntegerField(required=False, allow_null=True)
    quartier = serializers.CharField(required=False, allow_blank=True)
    coordonnees_gps = serializers.CharField(required=False, allow_blank=True)

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
                immeuble=immeuble,
                **occupant_data
            )

        # ✅ Créer les occupants bureaux
        for occupant_data in occupants_bureaux_data:
            OccupantBureaux.objects.create(
                immeuble=immeuble,
                **occupant_data
            )

        return immeuble

class AyantDroitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ayant_droits
        fields = '__all__'

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

class MoisNonMandateSerializer(serializers.Serializer):
    """Pour gérer les mois cochés"""
    mois_numero = serializers.IntegerField(min_value=1, max_value=12)
    statut = serializers.BooleanField(default=True)

class NonMandatementSerializer(serializers.ModelSerializer):
    mois_non_mandates = MoisNonMandateSerializer(many=True)

    class Meta:
        model = Non_Mandatement
        fields = '__all__'

class AvenantSerializer(serializers.ModelSerializer):
    ancien_bailleur_id = serializers.IntegerField(required=False, allow_null=True)
    nouveau_bailleur_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Avenants
        fields = '__all__'

class ContratSerializer(serializers.ModelSerializer):
    Periodicite_Reglement_id = serializers.IntegerField()

    class Meta:
        model = Contrats
        fields = '__all__'

    def validate_montant_loyer_mensuel(self, value):
        """Validation du montant"""
        if value and value <= 0:
            raise serializers.ValidationError(
                "Le montant du loyer doit être supérieur à 0"
            )
        return value

    def validate(self, data):
        """Validations croisées du contrat"""
        # Date de signature < Date d'effet
        if data.get('date_signature') and data.get('date_effet'):
            if data['date_signature'] > data['date_effet']:
                raise serializers.ValidationError({
                    'date_effet': 'La date d\'effet doit être postérieure à la date de signature'
                })

        # Si existence avenant, au moins 1 avenant requis
        if data.get('existence_avenant') and not data.get('avenants'):
            raise serializers.ValidationError({
                'avenants': 'Au moins un avenant est requis si existence_avenant est coché'
            })

        return data

    def create(self, contrat_data):
        """Créer le contrat avec toutes ses relations"""
        # Extraire les données imbriquées
        bailleur_data = contrat_data.pop('bailleur')
        avenants_data = contrat_data.pop('avenants', [])
        non_mandatements_data = contrat_data.pop('non_mandatements', [])

        # Créer le bailleur
        ayants_droit_data = bailleur_data.pop('ayants_droit', [])
        bailleur = Bailleurs.objects.create(**bailleur_data)

        # Créer les ayants droit
        for ayant_data in ayants_droit_data:
            Ayant_droits.objects.create(
                Bailleur=bailleur,
                **ayant_data
            )

        # Créer le contrat
        contrat = Contrats.objects.create(
            Bailleur=bailleur,
            **contrat_data
        )

        # Créer les avenants
        for avenant_data in avenants_data:
            Avenants.objects.create(
                contrat=contrat,
                **avenant_data
            )

        # Créer les non-mandatements
        for nm_data in non_mandatements_data:
            mois_data = nm_data.pop('mois_non_mandates', [])
            non_mandatement = Non_Mandatement.objects.create(
                contrat=contrat,
                **nm_data
            )

        return contrat

class PieceCollecteSerializer(serializers.Serializer):
    """Pour la table intermédiaire FicheCollecte-Piece"""
    piece_id = serializers.IntegerField()
    statut = serializers.BooleanField()
    nombre = serializers.IntegerField(default=0)

    class Meta:
        model = PieceCollectes
        fields = '__all__'

class FicheCollecteSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializer()
    contrat = ContratSerializer()
    pieces_collectees = PieceCollecteSerializer(many=True, required=False)

    class Meta:
        model = Collectes
        fields = '__all__'

    def create(self, validated_data):
        """Création avec gestion des relations imbriquées"""
        # Extraire les données imbriquées
        immeuble_data = validated_data.pop('immeuble')
        contrat_data = validated_data.pop('contrat')
        pieces_data = validated_data.pop('pieces_collectees', [])

        # Créer l'immeuble
        immeuble_serializer = ImmeubleSerializer()
        immeuble = immeuble_serializer.create(immeuble_data)

        # Créer le contrat
        contrat_serializer = ContratSerializer()
        contrat = contrat_serializer.create(contrat_data)

        # Créer la fiche de collecte
        fiche = Collectes.objects.create(
            Immeuble=immeuble,
            Contrat=contrat,
            **validated_data
        )

        # Créer les pièces collectées
        self._create_pieces_collectees(pieces_data, fiche)

        return fiche

    # Créer les pièces collectées
    def _create_pieces_collectees(self, pieces_data, fiche):
        """Créer les pièces collectées"""
        for piece_data in pieces_data:
            PieceCollectes.objects.create(
                fiche_collecte=fiche,
                piece_id=piece_data['piece_id'],
                statut=piece_data['statut'],
                nombre=piece_data['nombre']
            )
