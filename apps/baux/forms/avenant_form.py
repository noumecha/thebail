from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column, Fieldset, HTML
from dal import autocomplete

# avenants forms
class AvenantsForm(forms.ModelForm):
    class Meta:
        model = Avenants
        fields = (
            "Ref_Avenant",
            "Signataire",
            "Date_Signature",
            "Date_effet",
            "Modification_apportee",
            "Ancien_bailleur",
            "Nouveau_bailleur",
            #"Localite",
            "Montant_TTC_Mensuel_ancien",
            "Montant_TTC_Mensuel_Nouveau",
            #"Attestion_domicilliation_bancaire_ancien",
            "Attestion_domicilliation_bancaire_nouveau",
            "Duree_Contrat_Ancien",
            "Duree_Contrat_Nouveau",
            "Signataire",
            "Fichier_avenant"
        )
        labels = {
            "Ref_Avenant" : "Référence de l'avenant",
            "Signataire" : "Signataire",
            "Date_Signature" : "Date de signature",
            "Date_effet" : "Date de prise d'effet",
            "Modification_apportee" : "Modification apportée",
            "Ancien_bailleur" : "Nom & Prénom de l'ancien bailleur",
            "Nouveau_bailleur" : "Nom & Prénom du nouveau bailleur",
            #"Localite" : "Localité",
            "Montant_TTC_Mensuel_ancien" : "Montant Ancien Loyer Mensuel (TTC)",
            "Montant_TTC_Mensuel_Nouveau" : "Montant Nouveau Loyer Mensuel (TTC)",
            #"Attestion_domicilliation_bancaire_ancien" : "Ancienne Attestation de domicilliation bancaire",
            "Attestion_domicilliation_bancaire_nouveau" : "Nouvelle Attestation de domicilliation bancaire",
            "Duree_Contrat_Ancien" : "Ancienne Durée Contrat",
            "Duree_Contrat_Nouveau" : "Nouvelle Durée Contrat",
            "Fichier_avenant" : "Fichier numerique Avenant",
        }
        widgets = {
            "Date_Signature" : forms.TextInput(attrs={'type': 'date'}),
            "Date_effet" : forms.TextInput(attrs={'type': 'date'}),
            'Ancien_bailleur': autocomplete.ModelSelect2(url='baux:bailleur_autocomplete'),
            'Nouveau_bailleur': autocomplete.ModelSelect2(url='baux:bailleur_autocomplete'),

        }
    def __init__(self, *args, **kwargs):
        super(AvenantsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Ref_Avenant"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Signataire"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Date_effet"), css_class='overflow-hidden form-group col-md-4 mb-0'),
                        Column(FloatingField("Fichier_avenant"), css_class="overflow-hidden form-group col-md-4 mb-0"),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Modifications",
                    Row(
                        Column(FloatingField("Modification_apportee"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Ancien_bailleur"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Nouveau_bailleur"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        #Column(FloatingField("Localite"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel_ancien"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel_Nouveau"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        #Column(FloatingField("Attestion_domicilliation_bancaire_ancien"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Attestion_domicilliation_bancaire_nouveau"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Duree_Contrat_Ancien"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        Column(FloatingField("Duree_Contrat_Nouveau"), css_class='overflow-hidden form-group col-md-3 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Column(
                    HTML("""
                        <button type="button" 
                            class="btn btn-outline-primary add-form" 
                            id="avenant-collecte-add-btn"
                            data-formset="avenants"
                            data-table="avenant-collecte-table"> + Ajouter à la liste </button>
                    """
                    ),
                    css_class='overflow-hidden form-group col-md-3 mb-0'
                ),    
            )
        )