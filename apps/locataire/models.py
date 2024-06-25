from django.db import models
# Create your models here.
class TypePersonne(models.Model):
    libelle = models.CharField(max_length=255)
    
    def __str__(self):
        return self.libelle

class Locataire(models.Model):
    intitule = models.CharField(max_length=255)
    observation = models.TextField()
    type_personne = models.ForeignKey(TypePersonne, on_delete=models.CASCADE)

    def __str__(self):
        return self.intitule
