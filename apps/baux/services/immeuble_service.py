# services/immeuble_service.py
from apps.baux.models import Immeuble, ImmeubleRevetement, ImmeubleElement
from apps.baux.services.localisation_service import LocalisationService
from apps.baux.services.occupant_service import OccupantService

class ImmeubleService:

    @staticmethod
    def create(data: dict, collecte):

        immeuble = Immeuble.objects.create(
            collecte=collecte,
            type_construction_id=data["type_construction"]["id"],
            type_location_id=data["type_location"]["id"],
            statut_batisse_id=data["statut_batisse"]["id"]
        )

        # Localisation
        LocalisationService.create(data["localisation"], immeuble)

        # Revêtements
        for r in data.get("revetements", []):
            ImmeubleRevetement.objects.create(
                immeuble=immeuble,
                revetement_id=r["revetement_id"]
            )

        # Éléments de description
        for el in data["elements_description"]:
            if el["statut"]:
                ImmeubleElement.objects.create(
                    immeuble=immeuble,
                    element_id=el["element_id"],
                    quantite=el["quantite"]
                )

        # Occupants
        OccupantService.create_many(data["occupants"], immeuble)

        return immeuble
