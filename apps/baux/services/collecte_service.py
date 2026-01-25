# services/collecte_service.py
from django.db import transaction
from apps.baux.models import Collectes
from apps.baux.services.contrat_service import ContratService
from apps.baux.services.immeuble_service import ImmeubleService
from apps.baux.services.piece_service import PieceService

class CollecteService:

    @staticmethod
    @transaction.atomic
    def create(payload: dict):

        # 1. Création fiche de collecte
        collecte = Collectes.objects.create(
            Numero_fiche_de_collecte=payload["collecte"]["numero_fiche"],
            Date_de_collecte=payload["collecte"]["date_collecte"],
            Agent_id=payload["collecte"]["agent_collecte_id"],
            observation=payload["collecte"].get("observation_generale")
        )

        # 2. Immeuble
        immeuble = ImmeubleService.create(
            payload["immeuble"],
            collecte
        )

        # 3. Contrat
        contrat = ContratService.create(
            payload["contrat"],
            collecte
        )

        # 4. Pièces collectées
        PieceService.attach_to_collecte(
            payload["pieces_collectees"],
            collecte
        )

        return collecte
