from django.db import models
from apps.locataire.models import TypePersonne

# Create your models here.
class AyantDroit(models.Model):
    nom_prenom_ayant_droit = models.CharField(max_length=255)
    num_cni_ayant_droit = models.CharField(max_length=255)
    date_delivrance_cni_ayant_droit = models.DateField()
    reference_juridique = models.CharField(max_length=255)
    observation_ayant_droit = models.CharField(max_length=255)
    def __str__(self):
        return self.nom_prenom_ayant_droit

class Bailleur(models.Model):
    nom_prenom_bailleur = models.CharField(max_length=255)
    niu_bailleur = models.CharField(max_length=255)
    registre_commerce_bailleur = models.CharField(max_length=255)
    num_cni_bailleur = models.CharField(max_length=255)
    date_delivrance = models.DateField()
    nom_prenom_responsable = models.CharField(max_length=255)
    telephone_bailleur = models.CharField(max_length=255)
    adresse_bailleur = models.CharField(max_length=255)
    observaiton_bailleur = models.TextField()
    type_personne = models.ForeignKey(TypePersonne, on_delete=models.CASCADE)
    #num_cni_ayant_droit = models.ForeignKey(AyantDroit, on_delete=models.CASCADE)

    def __str__(self):
        return self.nom_prenom_bailleur