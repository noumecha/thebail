from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML

# Ayant droit form
class AyantDroitsForm(forms.ModelForm):
    class Meta:
        model = Ayant_droits
        fields = (
            "Nom_Prenom","Contact","Reference_Grosse","Date_prise_effet_grosse","Reference_certificat_non_effet",
            "Date_prise_effet_certificat_non_effet"
        )
        labels = {
            "Nom_Prenom" : "Noms & Prénoms",
            "Contact" : "Contact",
            "Reference_Grosse" : "Référence Grosse",
            "Date_prise_effet_grosse" : "Date de prise effet Grosse",
            "Reference_certificat_non_effet" : "Référence certificat non appel",
            "Date_prise_effet_certificat_non_effet" : "Date de prise effect certificat de non appel",
        }
        widgets = {
            "Date_prise_effet_grosse"  :  forms.TextInput(attrs={'type': 'date'}),
            "Date_prise_effet_certificat_non_effet"  :  forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AyantDroitsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Ayants Droits du Bailleurs",
                    Row(
                        Column(FloatingField("Nom_Prenom"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Contact"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Reference_Grosse"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_prise_effet_grosse"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Reference_certificat_non_effet"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_prise_effet_certificat_non_effet"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Column(
                    HTML("""
                        <button type="button"  class="btn btn-outline-primary add-form" id="ayantdroit-collecte-add-btn"
                        data-formset="ayantdroits" data-table="ayantdroit-collecte-table">
                        + Ajouter à la liste
                        </button>
                    """
                    ),
                    css_class='overflow-hidden form-group col-md-3 mb-0'
                ),
            )
        )