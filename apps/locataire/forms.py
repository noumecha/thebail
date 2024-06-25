from django.db import forms
from . import models

class LocataireForm(forms.ModelForm):
    class Meta:
        model = models.Locataire
        fields = ['intitule','observation','type_personne']

class TypePeronneForm(forms.ModelForm):
    class Meta:
        model = models.TypePersonne
        fields = ['libelle']