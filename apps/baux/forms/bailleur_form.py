from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML
from .nonmandatement_form import *
from .ayantdroit_form import *
from .immeuble_form import *

# bailleurs form
class BailleursForm(forms.ModelForm):

    class Meta:
        model = Bailleurs

        fields = (
            # information d'identifications
            "Type_personne",
            "Nom_prenom",
            "Raison_social",
            "NIU",
            "Maticule",
            "Telephone",
            "Domicille_siege_social_bailleur",
            "Type_id_bailleur",
            "Num_doc",
            "Date_delivrance_doc",
            "Document_identification",
            "Nom_Prenom_Representant",
            "Telephone_representant",
            "Statut_bailleur",
            # références bancaires
            "Banque",
            "RIB",
            "Document_RIB",
            "Intitule_compte",
            "Registre_commerce",
            "Regime_contribuable",
            "Code_centre",
            "Raison_social_abr",
            "Code_commune",
        )
        labels = {
            # identification
            "Type_personne" : "Personnalité Juridique",
            "Nom_prenom" : "Nom & Prénoms",
            "Raison_social" : "Raison Sociale",
            "NIU" : "NIU",
            "Maticule" : "Matricule",
            "Domicille_siege_social_bailleur" : "Domicille/siège sociale",
            "Telephone" : "Téléphone",
            "Type_id_bailleur" : "Type de pièce d'identité",
            "Num_doc" : "Numéro de la pièce d'identité",
            "Date_delivrance_doc" : "Date de délivrance",
            "Document_identification" : "Document d'identification",
            "Nom_Prenom_Representant" : "Représenté par",
            "Telephone_representant" : "Contact",
            "Statut_bailleur" : "Statut du bailleur",
            # references bancaires
            "Banque" : "Libelle Banque",
            "RIB" : "Numéro RIB",
            "Document_RIB" : "Document RIB",
            "Intitule_compte" : "Intitulé du compte",
            "Registre_commerce" : "Registre de commerce",
            "Regime_contribuable" : "Régime du contribuable",
            "Code_centre" : "Code centre",
            "Raison_social_abr" : "Raison sociale abrégée",
            "Code_commune" : "Code commune",
        }
        widgets = {
            'Date_delivrance_doc'  :  forms.TextInput(attrs={'type': 'date'}),
        }

    def partial_form(self):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False # remove form tags in the modal
        self.helper.disable_csrf = True # we use default csrf token in the template
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Type_personne"), css_class='overflow-hidden form-group col-md-12 mb-0 bailleur_type_personne'),
                        Column(FloatingField("Nom_prenom"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        #Column(FloatingField("Nationalite_bailleur"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Raison_social"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Maticule"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("Domicille_siege_social_bailleur"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Type_id_bailleur"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Num_doc"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_identification"), css_class='overflow-hidden form-group col-md-12 mb-0 bailleur_type_id'),
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone_representant"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_num_cni'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0"
            ),
        )
        return self.helper

    def __init__(self, *args, **kwargs):
        super(BailleursForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>a- Identification</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Type_personne"), css_class='overflow-hidden form-group col-md-12 mb-0 bailleur_type_personne'),
                        Column(FloatingField("Nom_prenom"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        #Column(FloatingField("Nationalite_bailleur"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Raison_social"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Maticule"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("Telephone"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Type_id_bailleur"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Num_doc"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_identification"), css_class='overflow-hidden form-group col-md-12 mb-0 bailleur_type_id'),
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone_representant"), css_class='overflow-hidden form-group col-md-6 mb-0 bailleur_num_cni'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>b- Références bancaires</h5>"),
                    css_class='overflow-hidden form-group col-md-12 mb-0'
                ),
            ),
            Row(
                Fieldset(
                    "Références bancaires",
                    Row(
                        Column(FloatingField("Banque"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("RIB"), css_class='overflow-hidden form-group col-md-6 mb-0 representant_type_id'),
                        Column(FloatingField("Document_RIB"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Intitule_compte"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Registre_commerce"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0",
            ),
            """Row(
                Fieldset(
                    "Attestation de non mandatement (Non-Encore payé)",
                    Formset("non_mandatements_formset"),
                    css_class="bg-white line__text border p-2 pt-4"
                )
            ),"""
        )
        self.helper.form_tag = False;self.fields['NIU'].required = False
        self.fields['Registre_commerce'].required = False; self.fields['Nom_Prenom_Representant'].required = False
        self.fields['Num_doc'].required = False;self.fields['Date_delivrance_doc'].required = False
        self.fields['Document_identification'].required = False
        self.fields['Telephone_representant'].required = False
