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

class ImmeubleSerializer(serializers.ModelSerializer):
    localisation = LocalisationSerializer()
    elements_description = ElementDescriptionLinkSerializer(many=True, write_only=True)
    occupants_residents = OccupantResidentSerializer(many=True, required=False)
    occupants_bureaux = OccupantBureauxSerializer(many=True, required=False)

    # Relations simples (FK)
    type_construction_id = serializers.IntegerField()
    type_location_id = serializers.IntegerField()
    statut_batisse_id = serializers.IntegerField()
    revetement_int_id = serializers.IntegerField(required=False, allow_null=True)
    revetement_ext_id = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Immeubles
        fields = '__all__'

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
    bailleur = BailleurSerializer()
    avenants = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True
    )
    non_mandatements = serializers.ListField(
        child=serializers.DictField(),
        required=False,
        allow_empty=True
    )

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


class PieceCollecteSerializer(serializers.Serializer):
    """Pour la table intermédiaire FicheCollecte-Piece"""
    piece_id = serializers.IntegerField()
    statut = serializers.BooleanField()
    nombre = serializers.IntegerField(default=0)

class FicheCollecteSerializer(serializers.ModelSerializer):
    immeuble = ImmeubleSerializer()
    contrat = ContratSerializer()
    pieces_collectees = PieceCollecteSerializer(many=True)

    class Meta:
        model = Collectes
        fields = '__all__'

    def create(self, validated_data):
        """Création avec gestion des relations imbriquées"""
        # Extraire les données imbriquées
        immeuble_data = validated_data.pop('immeuble')
        contrat_data = validated_data.pop('contrat')
        pieces_data = validated_data.pop('pieces_collectees', [])

        # Créer la fiche de collecte
        fiche = Collectes.objects.create(**validated_data)

        # Créer l'immeuble
        immeuble = self._create_immeuble(immeuble_data, fiche)

        # Créer le contrat
        contrat = self._create_contrat(contrat_data, fiche)

        # Créer les pièces collectées
        self._create_pieces_collectees(pieces_data, fiche)

        return fiche

    def _create_immeuble(self, immeuble_data, fiche):
        """Créer l'immeuble avec toutes ses relations"""
        # Extraire les données imbriquées
        localisation_data = immeuble_data.pop('localisation')
        elements_data = immeuble_data.pop('elements_description', [])
        occupants_residents_data = immeuble_data.pop('occupants_residents', [])
        occupants_bureaux_data = immeuble_data.pop('occupants_bureaux', [])

        # Créer la localisation
        localisation = Localisation.objects.create(**localisation_data)

        # Créer l'immeuble
        immeuble = Immeubles.objects.create(
            fiche_collecte=fiche,
            localisation=localisation,
            **immeuble_data
        )

        # Créer les liens avec ElementDescription
        for element_data in elements_data:
            ImmeubleElement.objects.create(
                immeuble=immeuble,
                element_id=element_data['element_id'],
                statut=element_data['statut'],
                nombre=element_data['nombre']
            )

        # Créer les occupants résidents
        for occupant_data in occupants_residents_data:
            Occupants.objects.create(
                immeuble=immeuble,
                **occupant_data
            )

        # Créer les occupants bureaux
        for occupant_data in occupants_bureaux_data:
            OccupantBureaux.objects.create(
                immeuble=immeuble,
                **occupant_data
            )

        return immeuble

    def _create_contrat(self, contrat_data, fiche):
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
                bailleur=bailleur,
                **ayant_data
            )

        # Créer le contrat
        contrat = Contrats.objects.create(
            fiche_collecte=fiche,
            bailleur=bailleur,
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

            # Créer les liens avec les mois

        return contrat

    def _create_pieces_collectees(self, pieces_data, fiche):
        """Créer les pièces collectées"""
        for piece_data in pieces_data:
            PieceCollectes.objects.create(
                fiche_collecte=fiche,
                piece_id=piece_data['piece_id'],
                statut=piece_data['statut'],
                nombre=piece_data['nombre']
            )
