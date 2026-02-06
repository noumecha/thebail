from rest_framework import serializers
from ..models import *
from .BailleurSerializer import BailleurSerializer
from .AvenantSerializer import AvenantSerializer
from .NonMandatementSerializer import NonMandatementSerializer

class ContratSerializer(serializers.ModelSerializer):
    Periodicite_Reglement_id = serializers.IntegerField()
    bailleur = BailleurSerializer()
    avenants = AvenantSerializer(many=True, required=False)
    non_mandatements = NonMandatementSerializer(many=True, required=False)

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
        # Check if bailleur exists in the data
        print("bailleur data", contrat_data)
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
        MONTH_MAP = {
            1: "janvier",
            2: "fevrier",
            3: "mars",
            4: "avril",
            5: "mai",
            6: "juin",
            7: "juillet",
            8: "aout",
            9: "septembre",
            10: "octobre",
            11: "novembre",
            12: "decembre",
        }

        for nm_data in non_mandatements_data:
            mois_data = nm_data.pop("mois_non_mandates", [])
            mois_flags = {field: False for field in MONTH_MAP.values()}
            for mois in mois_data:
                mois_numero = mois.get("mois_numero")
                if mois_numero in MONTH_MAP:
                    mois_flags[MONTH_MAP[mois_numero]] = True

            Non_Mandatement.objects.create(
                Contrat=contrat,
                **nm_data,
                **mois_flags
            )


        return contrat
