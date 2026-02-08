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

    def update(self, instance, validated_data):
        """Mettre à jour un contrat"""
        bailleur_data = validated_data.pop('bailleur', None)
        avenants_data = validated_data.pop('avenants', None)
        non_mandatements_data = validated_data.pop('non_mandatements', None)

        # Mettre à jour les champs simples du contrat
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # ✅ Mettre à jour le bailleur (update_or_create)
        if bailleur_data:
            ayants_droit_data = bailleur_data.pop('ayants_droit', None)

            if instance.Bailleur:
                # Mettre à jour le bailleur existant
                for attr, value in bailleur_data.items():
                    setattr(instance.Bailleur, attr, value)
                instance.Bailleur.save()
                bailleur = instance.Bailleur
            else:
                # Créer un nouveau bailleur
                bailleur = Bailleurs.objects.create(**bailleur_data)
                instance.Bailleur = bailleur
                instance.save()

            # ✅ Mettre à jour les ayants droit (update_or_create)
            if ayants_droit_data is not None:
                existing_ayant_ids = []
                for ayant_data in ayants_droit_data:
                    nom_prenom = ayant_data.get('Nom_Prenom_ayant_droit')
                    ayant, created = Ayant_droits.objects.update_or_create(
                        Bailleur=bailleur,
                        Nom_Prenom_ayant_droit=nom_prenom,
                        defaults=ayant_data
                    )
                    existing_ayant_ids.append(ayant.id)

                # Supprimer ceux qui ne sont plus présents
                Ayant_droits.objects.filter(
                    Bailleur=bailleur
                ).exclude(
                    id__in=existing_ayant_ids
                ).delete()

        # ✅ Mettre à jour les avenants (update_or_create)
        if avenants_data is not None:
            existing_avenant_ids = []
            for avenant_data in avenants_data:
                #ref_avenant = avenant_data.get('Ref_Avenant')
                avenant, created = Avenants.objects.update_or_create(
                    contrat=instance,
                    #Ref_Avenant=ref_avenant,
                    defaults=avenant_data
                )
                existing_avenant_ids.append(avenant.id)

            # Supprimer ceux qui ne sont plus présents
            Avenants.objects.filter(
                contrat=instance
            ).exclude(
                id__in=existing_avenant_ids
            ).delete()

        # ✅ Mettre à jour les non-mandatements (update_or_create)
        if non_mandatements_data is not None:
            existing_nm_ids = []
            for nm_data in non_mandatements_data:
                #ref_attestation = nm_data.get('Ref_Attestattion')
                nm, created = Non_Mandatement.objects.update_or_create(
                    Contrat=instance,
                    #Ref_Attestattion=ref_attestation,
                    defaults={
                        **nm_data,
                        'Bailleur': instance.Bailleur
                    }
                )
                existing_nm_ids.append(nm.id)

            # Supprimer ceux qui ne sont plus présents
            Non_Mandatement.objects.filter(
                Contrat=instance
            ).exclude(
                id__in=existing_nm_ids
            ).delete()

        return instance
