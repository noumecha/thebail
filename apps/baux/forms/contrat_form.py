from django import forms
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Field, HTML
from dal import autocomplete

# contrats forms
class ContratsForm(forms.ModelForm):
    class Meta:
        model = Contrats

        fields = ( 'Bailleur', 'Immeubles', 'Duree_Contrat', 'Signataire','Date_Signature', 'Date_Debut',
            'Periodicite_Reglement','Administration_beneficiaire', 'Montant_Charges_Mensuel','Visa_controlleur','Montant_Nap_Mensuel',
            'Banque', 'RIB', 'Document_RIB', 'Type_location','observation','Soumis_impot','Revisitable', 'statut_contrat', 'TypeContrat', 
            'nature_contrat', 'Montant_Taxe_Mensuel', 'Devise', 'Rabattement', 'Structure', 'Numero_contrat' #Locataire ,"Superficie_louer",'Ref_contrat',
        )
        labels = {
            "Bailleur": "Bailleur",  
            "Immeubles": "Imeubles Loués",
            #"Superficie_louer" : "Superficie louée",
            "TypeContrat" : "Type du Contrat",
            "Administration_beneficiaire" : "Section / Administration",
            "Structure" : "Chapitre", # Structure  
            "Duree_Contrat":" Durée du Contrat", 
            "Signataire":" Autorité Signataire du contrat",
            "Date_Signature":" Date de Signature du contrat",  
            "Date_Debut":" Date de prise d'effet du contrat ",
            "Numero_contrat":" N° du contrat",
            #"Ref_contrat":" Réference du contrat",
            "Periodicite_Reglement":"Periodicite de Reglement ",   
            "Montant_Charges_Mensuel":" Montant des Charges Mensuel",
            "Montant_Nap_Mensuel":"Montant LOYER Mensuel",  
            "Banque":" LIBELLE DE LA BANQUE",
            "RIB":"RIB",
            "Document_RIB" : "Document RIB",
            "statut_contrat":"Statut du contrat",
            "nature_contrat" : "Nature du Contrat",
            "Devise" : "Devise",
            "Montant_Taxe_Mensuel" : "Montant des taxes mensuelles",
            "Rabattement" : "Rabattement",
            "Type_location":"Type de location",
            "observation" : 'Observation',
            'Soumis_impot' : 'Soumis à l\'impôt',
            'Revisitable' : 'Revisitable en hausse',
            'Visa_controlleur' : 'Visa du controlleur',
        }
        widgets = {
            'observation': forms.Textarea(attrs={'rows':4, 'cols':10}),
            'Date_Debut'  : forms.TextInput(attrs={'type': 'date'}),
            'Date_Signature'  : forms.TextInput(attrs={'type': 'date'}),
            'Soumis_impot' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Revisitable' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Visa_controlleur' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Structure': autocomplete.ModelSelect2(url='baux:structure_autocomplete'),
            'Administration_beneficiaire': autocomplete.ModelSelect2(url='baux:administration_beneficiaire_autocomplete'),
            'Bailleur': autocomplete.ModelSelect2(url='baux:bailleur_autocomplete'),
        }
    def __init__(self, *args, **kwargs):
        super(ContratsForm, self).__init__(*args, **kwargs)
        # Prevent preloading millions of rows
        self.fields['Administration_beneficiaire'].queryset = Administrations.objects.none()
        self.fields['Structure'].queryset = Structures.objects.none()
        self.fields['Bailleur'].queryset = Bailleurs.objects.none()
        # Si l'instance a déjà une valeur (form update)
        if self.instance.pk:
            if self.instance.Administration_beneficiaire:
                self.fields['Administration_beneficiaire'].queryset = Administrations.objects.filter(
                    pk=self.instance.Administration_beneficiaire.pk
                )
            if self.instance.Structure:
                self.fields['Structure'].queryset = Structures.objects.filter(
                    pk=self.instance.Structure.pk
                )
            if self.instance.Bailleur:
                self.fields['Bailleur'].queryset = Bailleurs.objects.filter(
                    pk=self.instance.Bailleur.pk
                )

        # Si c’est un POST : recharger avec l’ID choisi
        if 'Administration_beneficiaire' in self.data:
            try:
                admin_id = int(self.data.get('Administration_beneficiaire'))
                self.fields['Administration_beneficiaire'].queryset = Administrations.objects.filter(pk=admin_id)
            except (ValueError, TypeError):
                pass

        if 'Structure' in self.data:
            try:
                structure_id = int(self.data.get('Structure'))
                self.fields['Structure'].queryset = Structures.objects.filter(pk=structure_id)
            except (ValueError, TypeError):
                pass

        if 'Bailleur' in self.data:
            try:
                bailleur_id = int(self.data.get('Bailleur'))
                self.fields['Bailleur'].queryset = Bailleurs.objects.filter(pk=bailleur_id)
            except (ValueError, TypeError):
                pass
        # 
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Numero_contrat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("TypeContrat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("nature_contrat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Debut"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire"), css_class='overflow-hidden form-group col-md-6 mb-0'),               
                        #Column(FloatingField("Superficie_louer"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Bailleur"), css_class='overflow-hidden form-group col-md-9 mb-0'),
                        Column(
                            HTML("""
                                <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addBailleurModal">
                                    + Ajouter
                                </button>
                            """
                            ),
                            css_class='overflow-hidden form-group col-md-3 mb-0'
                        ),                        
                        Column(
                            HTML("""
                                <label for="id_Immeubles">Selectionner un immeuble</label>
                                <div class="d-flex align-items-center">
                                    {{ form.Immeubles }}
                                    <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addImmeubleModal">
                                        + Ajouter
                                    </button>
                                </div>
                            """),
                            css_class='overflow-hidden form-group col-md-12 mb-3'
                        ),
                        Column(FloatingField("Type_location"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("statut_contrat"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Locataire",
                    Row(
                        Column(FloatingField("Administration_beneficiaire"), css_class='overflow-hidden form-group col-md-6 col-lg-6 mb-0'),
                        Column(FloatingField("Structure"), css_class='overflow-hidden form-group col-md-6 col-lg-6 mb-0'),
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Eléments financiers",
                    Row(
                        Column(FloatingField("Periodicite_Reglement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Nap_Mensuel"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Taxe_Mensuel"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Devise"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Rabattement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(
                            Field('Soumis_impot'),
                            css_class='overflow-hidden form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(
                            Field('Revisitable'),
                            css_class='overflow-hidden form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(
                            Field('Visa_controlleur'),
                            css_class='overflow-hidden form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(FloatingField("Banque"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("RIB"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_RIB"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges_Mensuel"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            FloatingField(
                "observation",
            ),
            Column(
                Submit(
                    "save",
                    "Enregistrer",
                    css_class="btn btn-lg btn-outline-primary"
                ),
                css_class='overflow-hidden form-group col-md-6 col-lg-6 mb-0'
            ),
        )
        self.fields['observation'].required = False
