from django.db import models

# Create your models here.
class TypeLocation(models.Model):
    libelle_type_location = models.CharField(max_length=255)
    
    def __str__(self):
        return self.libelle

class Contrat(models.Model):
    duree_contrat = models.IntegerField()
    date_debut_contrat = models.DateField(auto_now_add=True)
    signataire_contrat = models.CharField(max_length=255)
    date_signature_contrat = models.models.DateField(auto_now_add=True)
    ref_contrat = models.CharField(max_length=255)
    periodicite_reglement = models.CharField(max_length=255)
    montant_TTC_mensuel = models.FloatField()
    montant_charges_mensuel = models.FloatField()
    montant_NAP_mensuel = models.FloatField()
    banque_contrat = models.CharField(max_length=255)
    compte_bancaire_contrat = models.CharField(max_length=255)
    nom_CF_contrat = models.CharField(max_length=255)
    date_visa_CF_contrat = models.DateField(auto_now_add=True)
    etat_contrat = models.CharField(max_length=255)
    observation_contrat = models.TextField()
    type_location = models.ForeignKey(TypeLocation, on_delete=models.CASCADE)

    def __str__(self):
        return self.signataire_contrat
    