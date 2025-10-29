from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class RoleUtilisateur(models.TextChoices):
    ADMIN = 'administrateur', 'Administrateur'
    SUPERVISEUR = 'superviseur', 'Superviseur'
    AGENT = 'agent', 'Agent'
    GESTIONNAIRE = 'gestionnaire', 'Gestionnaire'
    RESPONSABLE = 'responsable', 'Responsable'

# Utilisateur personnalisé
class Utilisateur(AbstractUser):
    role = models.CharField(max_length=255, choices=RoleUtilisateur.choices, default=RoleUtilisateur.AGENT)
    #cellule = models.ForeignKey('administration.Cellule', on_delete=models.SET_NULL, null=True, blank=True, default=None)
    groups = models.ManyToManyField(
        Group,
        related_name="utilisateur_groups",  # <-- unique name
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="utilisateur_permissions",  # <-- unique name
        blank=True
    )
    # timestamp
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_name()
