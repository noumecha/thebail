from django import forms
from .models import Bailleur, AyantDroit

class BailleurForm(forms.ModelForm):
    class Meta:
        model = Bailleur
        fields = [
            'nom_prenom_bailleur',
            'niu_bailleur',
            'registre_commerce_bailleur',
            'num_cni_bailleur',
            'date_delivrance',
            'nom_prenom_responsable',
            'telephone_bailleur',
            'adresse_bailleur',
            'observaiton_bailleur',
            'type_personne',
            #'num_cni_ayant_droit'
        ]
        widgets = {
            'date_delivrance': forms.DateInput(attrs={'type': 'date'})
        }

class AyantDroitForm(forms.ModelForm):
    class Meta:
        model = AyantDroit
        fields = [
            'nom_prenom_ayant_droit',
            'num_cni_ayant_droit',
            'date_delivrance_cni_ayant_droit',
            'reference_juridique',
            'observation_ayant_droit'
        ]