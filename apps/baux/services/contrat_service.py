# services/contrat_service.py
from apps.baux.models import Contrat
from apps.baux.services.avenant_service import AvenantService
from apps.baux.services.bailleur_service import BailleurService
from apps.baux.services.non_mandatement_service import NonMandatementService

class ContratService:

    @staticmethod
    def create(data, collecte):

        contrat = Contrat.objects.create(
            collecte=collecte,
            type_contrat_id=data["type_contrat"]["id"],
            periodicite=data["periodicite_reglement"]["code"],
            numero=data["contrat_initial"]["numero"],
            montant_loyer=data["contrat_initial"]["montant_loyer_mensuel"]
        )

        # Avenants
        for a in data.get("avenants", []):
            AvenantService.create(a, contrat)

        # Bailleur
        BailleurService.attach(data["bailleur"], contrat)

        # Non-mandatements
        NonMandatementService.create_many(
            data.get("non_mandatements", []),
            contrat
        )

        return contrat
