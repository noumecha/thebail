from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML
from dal import autocomplete

# occupant pour bureaux
class OccupantBureauxForm(forms.ModelForm):
    class Meta:
        model = OccupantBureaux
        fields = (
            "Service_occupant_bureau","Administration_correspondante","Fonction_occupant_bureau","Ref_ActeJuridique_attribution",
            "Contact_occupant_bureau","Date_signature_acte_attribution","Immeuble",
        )
        labels = {
            "Service_occupant_bureau" : "Intitulé du service administratif",
            "Administration_correspondante" : "Administration correspondante",
            "Fonction_occupant_bureau" : "Fonction du plus haut responsable du service",
            "Ref_ActeJuridique_attribution" : "Référence de l'acte juridique d'attribution du MINDCAF",
            "Contact_occupant_bureau" : "Numéro de service",
            "Date_signature_acte_attribution" : "Date initiale d'occupation (jj/mm/aa)",
            "Immeuble" : "Imeuble",
        }

        widgets = {
            'Date_signature_acte_attribution' : forms.TextInput(attrs={'type': 'date'}),
            'Administration_correspondante': autocomplete.ModelSelect2(url='baux:administration_beneficiaire_autocomplete'),
            'Service_occupant_bureau': autocomplete.ModelSelect2(
                url='baux:service_autocomplete',
                forward=['Administration_correspondante'],
            ),
        }

    def __init__(self, *args, **kwargs):
        super(OccupantBureauxForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Occupation pour bureaux",
                    Row(
                        Column(FloatingField("Administration_correspondante"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Service_occupant_bureau"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Fonction_occupant_bureau"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique_attribution"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Contact_occupant_bureau"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Date_signature_acte_attribution"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Immeuble"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(
                            HTML("""
                                <button type="button"
                                    class="btn btn-outline-primary add-form"
                                    id="occupantbureau-collecte-add-btn"
                                    data-formset="occupants_bureau"
                                    data-table="occupantbureau-collecte-table">
                                    + Ajouter à la liste
                                </button>
                            """
                            ),
                            css_class='overflow-hidden form-group col-md-3 mb-0'
                        ),
                        Column(
                            HTML("""
                                <hr>
                                <table id="occupantbureau-collecte-table" class='bg-white table table-bordered mt-2'>
                                    <thead class='thead-dark'>
                                        <tr>
                                            <th>
                                                Intitulé du service administratif
                                            </th>
                                            <th>
                                                Administration correspondante
                                            </th>
                                            <th>
                                                Fonction du plus haut responsable du service
                                            </th>
                                            <th>
                                                Référence de l'acte juridique de l'attribution du MINDCAF
                                            </th>
                                            <th>
                                                Contact (Numero Camtel du Service)
                                            </th>
                                            <th>
                                                Date inital d'occupation (JJ/MM/AA)
                                            </th>
                                            <th>
                                                Action
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr id="empty-occupantbureau-row">
                                            <td colspan="7">Aucune occupation pour bureau ajouter ...</td>
                                        </tr>
                                    </tbody>
                                </table>
                            """
                            ),
                            css_class='overflow-hidden form-group col-md-12 mb-0'
                        ),
                        css_class='form-row'
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.helper.form_tag = False

# occupants form
class OccupantsForm(forms.ModelForm):
    class Meta:
        model = Occupants
        fields = (
            "Nom_Prenom_occupant_residence",
            "Administration_rattachement",
            "Fonction_occupant_residence",
            "Matricule_occupant_residence",
            "Ref_ActeJuridique_attribution",
            "Date_Signature_acte_juridique",
            "Telephone_occupant_residence",
            "NIU_occupant_residence","Immeuble",
        )
        labels = {
            "Nom_Prenom_occupant_residence" : "Noms & Prénoms",
            "Administration_rattachement" : "Administration de rattachement",
            "Fonction_occupant_residence" : "Fonction ou qualité de l'occupant",
            "Matricule_occupant_residence" : "Matricule de l'occupant",
            "NIU_occupant_residence" : "NIU de l'occupant",
            "Ref_ActeJuridique_attribution" : "Référence de l'acte juridique d'attribution",
            "Date_Signature_acte_juridique" : "Date de prise d'effet de l'acte(jj/mm/aa)",
            "Telephone_occupant_residence" : "Numéro de téléphone",
            "Immeuble" : "Imeuble",
        }

        widgets = {
            'Date_Signature_acte_juridique' : forms.TextInput(attrs={'type': 'date'}),
            'Administration_rattachement': autocomplete.ModelSelect2(url='baux:administration_beneficiaire_autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super(OccupantsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Occupation pour résidence",
                    Row(
                        Column(FloatingField("Nom_Prenom_occupant_residence"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Administration_rattachement"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Fonction_occupant_residence"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Matricule_occupant_residence"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("NIU_occupant_residence"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique_attribution"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Date_Signature_acte_juridique"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Telephone_occupant_residence"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Immeuble"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(
                            HTML("""
                                <button type="button"
                                    class="btn btn-outline-primary add-form"
                                    id="occupant-collecte-add-btn"
                                    data-formset="occupants_residence"
                                    data-table="occupant-collecte-table">
                                    + Ajouter à la liste
                                </button>
                            """
                            ),
                            css_class='overflow-hidden form-group col-md-3 mb-0'
                        ),
                        Column(
                                HTML("""
                                <tr>
                                <table id="occupant-collecte-table" class='bg-white table table-bordered mt-2'>
                                    <thead class='thead-dark'>
                                        <tr>
                                            <th>
                                                Noms & Prénoms
                                            </th>
                                            <th>
                                                Administration de tutelle de l'occupant
                                            </th>
                                            <th>
                                                Fonction ou qualité de l'occupant
                                            </th>
                                            <th>
                                                Matricule ou NIU
                                            </th>
                                            <th>
                                                Référence de l'acte juridique d'attribution
                                            </th>
                                            <th>
                                                Date de prise d'effet de l'acte (jj/mm/aa)
                                            </th>
                                            <th>
                                                Numero de téléphone
                                            </th>
                                            <th>
                                                Action
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        <tr id="empty-occupant-row">
                                            <td colspan="8">
                                                Aucune occupation de résidence ajouter ...
                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            """
                            ),
                            css_class='overflow-hidden form-group col-md-12 mb-0'
                        ),
                        css_class='form-row'
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="bg-secondary-subtle line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.helper.form_tag = False
