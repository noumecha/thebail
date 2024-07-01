from django import forms
from .models import Locataire, TypePersonne

class LocataireForm(forms.ModelForm):
    class Meta:
        model = Locataire
        fields = ['intitule','observation','type_personne']

class TypePeronneForm(forms.ModelForm):
    class Meta:
        model = TypePersonne
        fields = ['libelle']