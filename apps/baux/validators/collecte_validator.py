from django.core.exceptions import ValidationError
from datetime import date

def validate_fiche_collecte(fiche):
    erreurs = {}

    # règle 1 : date future interdite
    if fiche.date_collecte > date.today():
        erreurs["date_collecte"] = "La date de collecte ne peut pas être future."

    # règle 2 : métadonnées obligatoires
    meta = fiche.metadonnees or {}
    if "source" not in meta:
        erreurs["metadonnees.source"] = "La source est obligatoire."

    if "responsable" not in meta:
        erreurs["metadonnees.responsable"] = "Le responsable est obligatoire."

    # règle 3 : validation métier du statut
    if fiche.statut == "valide" and fiche.documents.count() == 0:
        erreurs["documents"] = "Une fiche validée doit contenir au moins un document."

    if erreurs:
        raise ValidationError(erreurs)
