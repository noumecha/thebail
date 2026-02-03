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
            "Nom_Prenom_ayant_droit","Contact_ayant_droit","Reference_Grosse_ayant_droit",
            "Date_delivrance_grosse","Reference_certificat_non_appel","Date_delivrance_certificat_non_appel"
        )
        labels = {
            "Nom_Prenom_ayant_droit" : "Noms & Prénoms",
            "Contact_ayant_droit" : "Contact",
            "Reference_Grosse_ayant_droit" : "Référence Grosse",
            "Date_delivrance_grosse" : "Date de délivrance Grosse",
            "Reference_certificat_non_appel" : "Référence certificat non appel",
            "Date_delivrance_certificat_non_appel" : "Date de prise effect certificat de non appel",
        }
        widgets = {
            "Date_delivrance_grosse"  :  forms.TextInput(attrs={'type': 'date'}),
            "Date_delivrance_certificat_non_appel"  :  forms.TextInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(AyantDroitsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Ayants Droits du Bailleurs",
                    Row(
                        Column(FloatingField("Nom_Prenom_ayant_droit"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Contact_ayant_droit"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Reference_Grosse_ayant_droit"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_delivrance_grosse"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Reference_certificat_non_effet"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_delivrance_certificat_non_appel"), css_class='overflow-hidden form-group col-md-3 mb-0'),
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
