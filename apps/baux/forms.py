from django import forms
from django.forms import inlineformset_factory
from .models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import HTML
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Button, Field
from dal import autocomplete
from crispy_forms.layout import LayoutObject, HTML
from django.template.loader import render_to_string

# extedns crispy form capabilities 
class Formset(LayoutObject):
    def __init__(self, formset_name_in_context, template="baux/formset_template.html"):
        self.formset_name_in_context = formset_name_in_context
        self.template = template

    def render(self, form, context, template_pack=None, **kwargs):
        formset = context[self.formset_name_in_context]
        return render_to_string(self.template, {'formset': formset})

# locataires forms
class LocatairesForm(forms.ModelForm):
    class Meta:
        model = Locataires

        fields = ('Intitule','NIU','Nom_Prenom_Representant','Peut_payer','Num_Cni','Date_delivrance_cni','Type_personne','Observation')
        labels = {
            "Intitule": " Autorité signataire",
            "NIU": "NIU(idientifiant unique DGI)",
            "Nom_Prenom_Representant": " Nom et prenoms du Representant" ,
            "Num_Cni": " Numero carte d'identité nationnale",
            "Date_delivrance_cni" :"date de delivrance CNI" ,
            "Type_personne": "Type de personne",
            "Observation": "Observation" ,
            "Peut_payer" : "Peut payer",
        }
        
        widgets = {
            'Observation': forms.Textarea(attrs={'rows':4, 'cols':10}),
            'Date_delivrance_cni'  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(LocatairesForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations locataire",
                    Row(
                        Column(FloatingField("Intitule"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Peut_payer"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='form-group col-md-6 mb-0'),  
                        Column(FloatingField("Num_Cni"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_cni"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_personne"), css_class='form-group col-md-6 mb-0'),  
                        css_class='form-row' 
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0",
            ),
            FloatingField("Observation"),
        )
        self.fields['Observation'].required = False
        self.helper.form_tag = False
        self.fields['NIU'].required = False
        self.fields['Num_Cni'].required = False
        self.fields['Date_delivrance_cni'].required = False
          
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
                        Column(FloatingField("Type_personne"), css_class='form-group col-md-12 mb-0 bailleur_type_personne'),   
                        Column(FloatingField("Nom_prenom"), css_class='form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        #Column(FloatingField("Nationalite_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Raison_social"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Maticule"), css_class='form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Type_id_bailleur"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Num_doc"), css_class='form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_identification"), css_class='form-group col-md-12 mb-0 bailleur_type_id'),  
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone_representant"), css_class='form-group col-md-6 mb-0 bailleur_num_cni'),
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
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Type_personne"), css_class='form-group col-md-12 mb-0 bailleur_type_personne'),   
                        Column(FloatingField("Nom_prenom"), css_class='form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        #Column(FloatingField("Nationalite_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Raison_social"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Maticule"), css_class='form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Type_id_bailleur"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Num_doc"), css_class='form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_identification"), css_class='form-group col-md-12 mb-0 bailleur_type_id'),  
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone_representant"), css_class='form-group col-md-6 mb-0 bailleur_num_cni'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0" 
            ),
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>b- Références bancaires</h5>"),
                    css_class='form-group col-md-12 mb-0'
                ),
            ),
            Row(
                Fieldset(
                    "Références bancaires",
                    Row(
                        Column(FloatingField("Banque"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("RIB"), css_class='form-group col-md-6 mb-0 representant_type_id'),
                        Column(FloatingField("Document_RIB"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Intitule_compte"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Registre_commerce"), css_class='form-group col-md-6 mb-0'),
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
        self.fields['Telephone_representant'].required = False


# localisation form
class LocalisationForm(forms.ModelForm):
    class Meta:
        model = Localisation

        fields = ('Quartier','Observation','arrondissement','pays','region','departement','Type_localisation','Ville','Rue')
        labels = {
            "Quartier": "Nom du Quartier ",
            "arrondissement": "Arrondissement",
            "departement": "Département",
            "region" : "Region",
            "pays": " Pays" ,
            "Observation": "Observation" ,
            "Type_localisation" : "Type de localisation",
            "Ville" : "Ville",
            "Rue" : "Rue",
        }

        widgets = {
          'Observation': forms.Textarea(attrs={'rows':4, 'cols':10}),
        }
    def __init__(self, *args, **kwargs):
        super(LocalisationForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Coordonnées géorgraphiques",
                    Row(
                        Column(FloatingField("Type_localisation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("pays"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ville"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Rue"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("region"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("departement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Quartier"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            FloatingField("Observation"),
        )
        self.helper.form_tag = False;self.fields['Observation'].required = False


# occupants form
class OccupantsForm(forms.ModelForm):
    class Meta:
        model = Occupants
        fields = (
            "Nom_Prenom","Administration_tutelle","Fonction","Matricule","NIU","Ref_ActeJuridique",
            "Date_Signature_acte_juridique","Telephone","Immeuble",
        )
        labels = {
            "Nom_Prenom" : "Noms & Prénoms",
            "Administration_tutelle" : "Administration de tutelle de l'occupant",
            "Fonction" : "Fonction ou qualité de l'occupant",
            "Matricule" : "Matricule de l'occupant",
            "NIU" : "NIU de l'occupant",
            "Ref_ActeJuridique" : "Référence de l'acte juridique d'attribution",
            "Date_Signature_acte_juridique" : "Date de prise d'effet de l'acte(jj/mm/aa)",
            "Telephone" : "Numéro de téléphone",
            "Immeuble" : "Imeuble",
        }

        widgets = {
            'Date_Signature_acte_juridique' : forms.TextInput(attrs={'type': 'date'}),
            'Administration_tutelle': autocomplete.ModelSelect2(url='baux:administration_beneficiaire_autocomplete'),
        }
        
    def __init__(self, *args, **kwargs):
        super(OccupantsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Occupation pour résidence",
                    Row(
                        Column(FloatingField("Nom_Prenom"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Administration_tutelle"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Matricule"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature_acte_juridique"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Immeuble"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            HTML("""
                                <button type="button" class="btn btn-sm btn-outline-primary add-form" data-prefix="{{ formset.prefix }}">
                                    + Ajouter
                                </button>
                            """
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),  
                        css_class='form-row' 
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.helper.form_tag = False

class OccupantBureauxForm(forms.ModelForm):
    class Meta:
        model = OccupantBureaux
        fields = (
            "Service","Administration_correspondante","Fonction","Ref_ActeJuridique_attribution","Contact","Date_initial_acte_occupation","Immeuble",
        )
        labels = {
            "Service" : "Intitulé du service administratif",
            "Administration_correspondante" : "Administration correspondante",
            "Fonction" : "Fonction du plus haut responsable du service",
            "Ref_ActeJuridique_attribution" : "Référence de l'acte juridique d'attribution du MINDCAF",
            "Contact" : "Contact (Numéro Camtel du service)",
            "Date_initial_acte_occupation" : "Date initial d'occupation (jj/mm/aa)",
            "Immeuble" : "Imeuble",
        }

        widgets = {
            'Date_initial_acte_occupation' : forms.TextInput(attrs={'type': 'date'}),
            'Service': autocomplete.ModelSelect2(url='baux:service_autocomplete'),
            'Administration_correspondante': autocomplete.ModelSelect2(url='baux:administration_beneficiaire_autocomplete'),
        }
        
    def __init__(self, *args, **kwargs):
        super(OccupantBureauxForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Occupation pour bureaux",
                    Row(
                        Column(FloatingField("Service"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Administration_correspondante"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique_attribution"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Contact"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_initial_acte_occupation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Immeuble"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            HTML("""
                                <button type="button" class="btn btn-sm btn-outline-primary add-form" data-prefix="{{ formset.prefix }}">
                                    + Ajouter
                                </button>
                            """
                            ),
                            css_class='form-group col-md-3 mb-0'
                        ),   
                        css_class='form-row' 
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.helper.form_tag = False


# recensement form
class RecensementsForm(forms.ModelForm):
    class Meta:
        model = Recensements

        fields = (
            "Agent_recenseur", "Type_immeuble", "Type_mur", 
            "Couleur", "Emprise_au_sol", "Description", "Immeuble", #"Situation_de_la_batisse"
        )

        labels = {
            "Type_immeuble" : "Type immeuble ",
            #"Construction" : "Type de construction",
            "Type_mur" : "Type de Mur",
            "Couleur" : "Ajouter la couleur",
            "Emprise_au_sol" : "Emprise au sol",
            "Description" : "Autres informations",
            "Immeuble"  : "Immeuble",
            #"Situation_de_la_batisse" : "Etat de la batisse",
            "Agent_recenseur" : "Nom Agent recenseur"
        }

        widgets = {
          'Description' : forms.Textarea(attrs={'rows':4, 'cols':10}),
        }

    def __init__(self, *args, **kwargs):
        super(RecensementsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations sur le recenseur",
                    Row(
                        Column(FloatingField("Agent_recenseur"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Informations sur l'immeuble",
                    Row(
                        Column(FloatingField("Immeuble"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Description", css_class="form-group col-md-12 mb-0 mt-1")),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Caractéristiques du batiment",
                    Row(
                        #Column(FloatingField("Construction"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Emprise_au_sol"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Type_mur"), css_class='form-group col-md-6 mb-0'),            
                        Column(FloatingField("Couleur"), css_class='color_class form-group col-md-6 mb-0'),            
                        Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Situation_de_la_batisse"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.fields['Description'].required = False   

# type immeuble form
class TypeConstructionsForm(forms.ModelForm):
    class Meta:
        model = TypeConstructions

        fields = ('libelle', 'description')
        labels = {
            'libelle': "Type d'immeuble",
            'description': "Description du type d'immeuble",
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(TypeConstructionsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("libelle"), css_class='form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )
    
class RevetementIntsForm(forms.ModelForm):
    class Meta:
        model = RevetementInts

        fields = ('libelle', 'description')
        labels = {
            'libelle': "Revetement interieure",
            'description': "Description du revetement interieure",
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RevetementIntsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("libelle"), css_class='form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )

class RevetementExtsForm(forms.ModelForm):
    class Meta:
        model = RevetementExts

        fields = ('libelle', 'description')
        labels = {
            'libelle': "Revetement exterieure",
            'description': "Description du revetement exterieure",
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RevetementExtsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("libelle"), css_class='form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )

# element de description form
class ElementDeDescriptionForm(forms.ModelForm):
    class Meta:
        model = ElementDeDescription
        fields = ("libelle",)
        labels = {
            "libelle": "Libelle",
        }
        def __init__(self, *args, **kwargs):
            super(ElementDeDescriptionForm, self).__init__(*args, **kwargs)
            self.helper =  FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column(FloatingField("libelle"), css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),         
            )

# immeuble element formset
class ImmeubleElementForm(forms.ModelForm):
    class Meta:
        model = ImmeubleElement
        fields = ("element", "nombre", "statut")
        labels = {
            "element": "Elément",
            "nombre": "Nombre",
            "statut": "Statut (coché pour activé)",
        }
        widgets = {
            'statut' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        def __init__(self, *args, **kwargs):
            super(ImmeubleElementForm, self).__init__(*args, **kwargs)
            self.helper =  FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column(FloatingField("statut"), css_class='form-group col-md-6 mb-0'),
                    Column(FloatingField("element"), css_class='form-group col-md-12 mb-0'),
                    Column(FloatingField("nombre"), css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                        
            )

# piece form
class FichiersPieceForm(forms.ModelForm):
    class Meta:
        model = FichiersPiece
        fields = ("fichier",)

    def __init__(self, *args, **kwargs):
        super(FichiersPieceForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = False
        self.helper.layout = Layout(
            Row(Column("fichier", css_class="col-md-12"))
        )

FichiersPieceFormSet = inlineformset_factory(
    PieceCollectes, FichiersPiece,
    form=FichiersPieceForm,
    extra=0,  # nombre ajusté dynamiquement en JS
    can_delete=True
)

class PiecesForm(forms.ModelForm):
    class Meta:
        model = Pieces
        fields = ("libelle",)
        labels = {
            "libelle": "Libelle",
        }
        def __init__(self, *args, **kwargs):
            super(PiecesForm, self).__init__(*args, **kwargs)
            self.helper =  FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column(FloatingField("libelle"), css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),         
            )

class PieceCollectesForm(forms.ModelForm):
    class Meta:
        model = PieceCollectes
        fields = (
            "Piece", "statut", "nombre"
        )
        labels = {
            "Piece": "Pièce",
            "statut": "Nombre",
            "nombre": "Statut (coché pour activé)",
        }
        widgets = {
            'statut' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        def __init__(self, *args, **kwargs):
            super(PieceCollectesForm, self).__init__(*args, **kwargs)
            self.helper =  FormHelper()
            self.helper.layout = Layout(
                Row(
                    Column(FloatingField("statut"), css_class='form-group col-md-6 mb-0'),
                    Column(FloatingField("piece"), css_class='form-group col-md-12 mb-0'),
                    Column(FloatingField("nombre"), css_class='form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                        
            )

# collectes form
class CollectesForm(forms.ModelForm):
    class Meta:
        model = Collectes

        fields = (
            # informations du contrat et sur le collecteur 
            "Numero_fiche_de_collecte",
            "Agent_de_collecte",
            "Matricule_agent_de_collecte",
            "Date_de_collecte",
            "TypeContrat",
            # informations contrat initial
            "Numero_contrat",
            "Date_signature_contrat",
            "Fonction_signataire_contrat",
            "Date_effet_contrat",
            "Regime_fiscal_contrat",
            "Montant_loyer_mensuel",
            "Devise",
            # avenant informations 
            "Existance_avenant",
            "Existance_visa_budgetaire",
            "observation",
            "Periodicite_Reglement",
        )
        labels = {
            # informations du contrat et sur le collecteur
            "Numero_fiche_de_collecte" : "Fiche de collecte N°",
            "Agent_de_collecte" : "Agent de collecte",
            "Matricule_agent_de_collecte" : "Matricule de l'agent de collecte",
            "Date_de_collecte" : "Date de collecte",
            "TypeContrat" : "Typologie du contrat",
            # informations contrat initial
            "Numero_contrat" : "Référence ou Numéro du contrat",
            "Date_signature_contrat" : "Date de signature",
            "Fonction_signataire_contrat" : "Qualité ou fonction du signataire du contrat",
            "Date_effet_contrat" : "Date de prise d'effet",
            "Regime_fiscal_contrat" : "Régime fiscal",
            "Montant_loyer_mensuel" : "Montant du loyer mensuel(TTC)",
            "Devise" : "Devise",
            # avenant informations
            "Existance_avenant" : "Existance d'au moins un avenant ?",
            "Existance_visa_budgetaire" : "Existance d'un visa budgétaire ?",
            "observation" : "Observation",
            "Periodicite_Reglement" : "Périodicité de règlement selon le contrat",
        }
        widgets = {
            'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)

        # after saving the immeuble, create/update ImmeubleElement
        for piece in Pieces.objects.all():
            statut = self.cleaned_data.get(f"piece_{piece.id}_statut")
            nombre = self.cleaned_data.get(f"piece_{piece.id}_nombre")

            if statut:
                obj, created = PieceCollectes.objects.update_or_create(
                    collecte=instance, piece=piece,
                    defaults={"statut": statut, "nombre": nombre or 0}
                )
            else:
                # If unchecked, delete existing link if it exists
                PieceCollectes.objects.filter(collecte=instance, piece=piece).delete()

        return instance

    def __init__(self, *args, **kwargs):
        super(CollectesForm, self).__init__(*args, **kwargs)
        # Dynamically create fields for each pieces
        pieces = list(Pieces.objects.all())
        # 1) Create dynamic fields
        for el in pieces:
            self.fields[f"piece_{el.pk}_statut"] = forms.BooleanField(
                required=False, label=el.libelle
            )
            self.fields[f"piece_{el.pk}_nombre"] = forms.IntegerField(
                required=False, min_value=0, initial=0, label="",
            )
            # Optional: set initial values when editing an existing Collecte
            if self.instance and self.instance.pk:
                try:
                    link = PieceCollectes.objects.get(collecte=self.instance, piece=el)
                    self.fields[f"piece_{el.pk}_statut"].initial = link.statut
                    self.fields[f"piece_{el.pk}_nombre"].initial = link.nombre
                except PieceCollectes.DoesNotExist:
                    pass
        # 2) Build the dynamic rows for the layout
        piece_rows = []
        for el in pieces:
            piece_rows.append(
                Column(
                    Field(f"piece_{el.pk}_statut", css_class=""),
                    Field(f"piece_{el.pk}_nombre", css_class="ms-2 w-50"),
                    css_class="m-0 col-md-4 d-flex align-items-center justify-content-center"
                )
            )
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            # informations sur le contrat
            Row(
                Column(
                    HTML("<h4 class='bg-gray text-white p-2 mt-2 mb-2'>SECTION 1. INFORMATIONS CONTRACTUELLES</h4>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>I. Identification</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Identifications",
                    Row(
                        Column(FloatingField("Numero_fiche_de_collecte"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Agent_de_collecte"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Matricule_agent_de_collecte"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_de_collecte"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("TypeContrat"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            HTML("""
                                <label for="id_TypeContrat">Selectionner un type de contrat</label>
                                <div class="d-flex align-items-center">
                                    {{ form.TypeContrat }}
                                    <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addTypeContratModal">
                                        + Ajouter
                                    </button>
                                </div>
                            """),
                            css_class='form-group col-md-12 mb-3'
                        ),
                        css_class="form-row"
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # Element juridiques section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>II. Elements juridiques</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                # title of subsection
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>a- Contrat Initial</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                # content
                Fieldset(
                    "Contrat Initial",
                    Row(
                        Column(FloatingField("Numero_contrat"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Date_signature_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction_signataire_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_effet_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Regime_fiscal_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_loyer_mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Devise"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row"
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Existence d'avenant / visa budgétaire",
                    Row(
                        Column(FloatingField("Existance_avenant"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Existance_visa_budgetaire"), css_class='form-group col-md-12 mb-0'),
                        Column(
                            HTML("<h5 class='text-bold fw bg-secondary-subtle'>b- Avenants liés au Contrat Initial</h5>"), 
                            css_class='form-group col-md-12 mb-0'
                        ),
                        Formset("avenants_formset"),
                        Column(FloatingField("observation"), css_class='form-group col-md-12 mb-0'),
                        css_class="form-row"
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>c- Périodicité de règlement selon le contrat</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                Column(FloatingField("Periodicite_Reglement"), css_class='form-group col-md-12 mb-0'),
                css_class="p-3 pt-0"
            ),
            # Bailleur section 
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>III. bailleur</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Formset("bailleurs_formset"),
                css_class="p-3 pt-0"
            ),
            Row(
                Column(
                    HTML("<h5 class='text-bold fw bg-secondary-subtle'>c- Ayants Droits du Bailleurs</h5>"),
                    css_class='form-group col-md-12 mb-0'
                ),
                Formset("ayants_droits_formset"),
                css_class="p-3 pt-0"
            ),
            # Non-Mandatement section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>IV. attestion de non-mandatement (non-encore payé)</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Formset("non_mandatements_formset"),
                css_class="p-3 pt-0"
            ),
            # Immeuble Section
            Row(
                Column(
                    HTML("<h4 class='bg-gray text-white p-2 mt-2 mb-2'>SECTION 2. INFORMATIONS SUR L'IMMEUBLE</h4>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Formset("immeubles_formset"),
                css_class="p-3 pt-0"
            ),
            #Row(
            #    Column(
            #        HTML("<h5 class='text-uppercase bg-secondary-subtle'>V. Occupants actuels de l'immeuble </h5>"), 
            #        css_class='form-group col-md-12 mb-0'
            #    ),
            #    css_class='form-row'
            #),
            Row(
                Formset("occupants_residence_formset"),
                css_class="p-3 pt-0"
            ),
            Row(
                Formset("occupants_bureau_formset"),
                css_class="p-3 pt-0"
            ),
            # Pièces collectées
            Row(
                Column(
                    HTML("<h4 class='text-uppercase bg-gray text-white p-2 mt-2 mb-2'>SECTION 3. pièces collectées</h4>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Pieces Collectées",
                    Row(
                        *piece_rows,
                        css_class="form-row"
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-2"
            ),
            Column(
                Submit(
                    "save",
                    "Enregistrer",
                    css_class="btn btn-lg btn-outline-primary"
                ),
                css_class='form-group col-md-6 col-lg-6 mb-0'
            ),
        )
        self.helper.form_tag = False

# immeubles form
class ImmeublesForm(forms.ModelForm):
    class Meta:
        model = Immeubles

        fields = (
            # idenfification fields
            "Designation","Construction","Date_Construction","Type_location","Nombre_de_pieces", "Norme","Superficie_louer",
            # localisation fields
            "Type_localisation","pays","Ville","Rue","region","departement","arrondissement","Quartier","Coordonee_gps",
            # etat physique du batiement fields
            "Situation_de_la_batisse","Revetement_interieure","Revetement_exterieure", "observation",
        )
        labels = {
            # idenfification labels
            "Designation": " Désignation du Bien",
            "Construction" : "Type de construction",
            "Date_Construction" : "Date de construction",
            "Nombre_de_pieces" : "Nombre total de pièces",
            "Superficie_louer" : "Superficie louée(m²)",
            "Norme" : "Norme de Cadastrale",
            "Type_location" : "Type de location",
            # etat physique du batiement fields
            "Revetement_interieure" : "Revetement interieure",
            "Revetement_exterieure" : "Revetement exterieure",
            "observation" : "Observation",
            "Situation_de_la_batisse" : "Etat de la batisse",
            # localisation labels
            "Type_localisation" : "Type de localisation",
            "pays" : "Pays",
            "Ville" : "Ville",
            "Rue" : "Rue",
            "region" : "Région",
            "departement" : "Département",
            "arrondissement" : "Arrondissement",
            "Quartier" : "Quartier",
            "Coordonee_gps" : "Coordonnées GPS",
        }
        widgets = {
            'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=commit)

        # after saving the immeuble, create/update ImmeubleElement
        for element in ElementDeDescription.objects.all():
            statut = self.cleaned_data.get(f"element_{element.id}_statut")
            nombre = self.cleaned_data.get(f"element_{element.id}_nombre")

            if statut:  # if element is selected
                obj, created = ImmeubleElement.objects.update_or_create(
                    immeuble=instance, element=element,
                    defaults={"statut": statut, "nombre": nombre or 0}
                )
            else:
                # If unchecked, delete existing link if it exists
                ImmeubleElement.objects.filter(immeuble=instance, element=element).delete()

        return instance

    def partial_form(self):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_tag = False # remove form tags in the modal
        helper.disable_csrf = True # we use default csrf token in the template
        helper.layout = Layout(
            Row(
                Fieldset(
                        "I. Identification",
                        Row(
                            Column(FloatingField("Designation"), css_class='form-group col-md-12 mb-0'),
                            Column(FloatingField("Construction"), css_class='form-group col-md-6 mb-0'),
                            Column(FloatingField("Date_Construction"), css_class='form-group col-md-6 mb-0'), 
                            Column(FloatingField("Nombre_de_pieces"), css_class='form-group col-md-4 mb-0'),
                            Column(FloatingField("Superficie_louer"), css_class='form-group col-md-4 mb-0'), 
                            Column(FloatingField("Norme"), css_class='form-group col-md-4 mb-0'),    
                            Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'),    
                            #Column(FloatingField("Type_construction"), css_class='form-group col-md-6 mb-0'),
                            css_class='form-row'
                        ),
                        css_class="bg-white line__text border p-2 pt-4"
                    ),
                    css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "II. Localisation",
                    Row(
                        #Column(FloatingField("Localisation"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Type_localisation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("pays"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ville"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Rue"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("region"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("departement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Quartier"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "III. Etat physique du batiment",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Revetement_interieure"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Revetement_exterieure"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("observation"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "IV. Description de la batisse",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            """Row(
                Fieldset(
                    "Occupants Pour résidence",
                    Formset(OccupantsFormSet("occupants_formset")),
                    css_class="bg-white line__text border p-2 pt-4"
                )
            ),
            Row(
                Fieldset(
                    "Occupants Pour bureaux",
                    Formset("occupants_bureau_formset"),
                    css_class="bg-white line__text border p-2 pt-4"
                )
            )"""
        )
        return helper

    def __init__(self, *args, **kwargs):
        super(ImmeublesForm, self).__init__(*args, **kwargs)
        # Dynamically create fields for each element
        elements = list(ElementDeDescription.objects.all())
        # 1) Create dynamic fields
        for el in elements:
            self.fields[f"element_{el.pk}_statut"] = forms.BooleanField(
                required=False, label=el.libelle
            )
            self.fields[f"element_{el.pk}_nombre"] = forms.IntegerField(
                required=False, min_value=0, initial=0, label="",
            )
            # Optional: set initial values when editing an existing Immeuble
            if self.instance and self.instance.pk:
                try:
                    link = ImmeubleElement.objects.get(immeuble=self.instance, element=el)
                    self.fields[f"element_{el.pk}_statut"].initial = link.statut
                    self.fields[f"element_{el.pk}_nombre"].initial = link.nombre
                except ImmeubleElement.DoesNotExist:
                    pass
        # 2) Build the dynamic rows for the layout
        element_rows = []
        for el in elements:
            element_rows.append(
                Column(
                    Field(f"element_{el.pk}_statut", css_class=""),
                    Field(f"element_{el.pk}_nombre", css_class="ms-2 w-50"),
                    css_class="m-0 col-md-4 d-flex align-items-center justify-content-center"
                )
            )
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>I. Identification</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Identification",
                    Row(
                        Column(FloatingField("Designation"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Construction"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Construction"), css_class='form-group col-md-6 mb-0'), 
                        Column(FloatingField("Nombre_de_pieces"), css_class='form-group col-md-6 mb-0'), 
                        Column(FloatingField("Superficie_louer"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Norme"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'), 
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>II. Localisation</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Localisation",
                    Row(
                        Column(FloatingField("Type_localisation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("pays"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ville"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Rue"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("region"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("departement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Quartier"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # title of the section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>III. Etat physique du batiment</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row (
                Fieldset(
                    "Etat physique du batiment",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Revetement_interieure"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Revetement_exterieure"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("observation"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # Dynamic section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>IV. Description de la batisse</h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            Row(
                Fieldset(
                    "Description de la batisse",
                    Row(
                        *element_rows,
                        css_class="form-row"
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            # Occupant section
            Row(
                Column(
                    HTML("<h5 class='text-uppercase bg-secondary-subtle'>V. Occupants actuels de l'immeuble </h5>"), 
                    css_class='form-group col-md-12 mb-0'
                ),
                css_class='form-row'
            ),
            #Row(
            #    Fieldset(
            #        "Occupants Pour résidence",
            #        Formset("occupants_residence_formset"),
            #        css_class="bg-white line__text border p-2 pt-4"
            #    )
            #),
            #Row(
            #    Fieldset(
            #        "Occupants Pour bureaux",
            #        Formset("occupants_bureau_formset"),
            #        css_class="bg-white line__text border p-2 pt-4"
            #    )
            #)
        )     
        self.fields['Date_Construction'].required = False;   


# contrats forms 
class TypeContratsForm(forms.ModelForm):
    class Meta:
        model = TypeContrats

        fields = ('libelle', 'description')
        labels = {
            'libelle': "Type de contrat",
            'description': "Description du type de contrat",
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(TypeContratsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("libelle"), css_class='form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )

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
                        Column(FloatingField("Numero_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("TypeContrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("nature_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire"), css_class='form-group col-md-6 mb-0'),               
                        #Column(FloatingField("Superficie_louer"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Bailleur"), css_class='form-group col-md-9 mb-0'),
                        Column(
                            HTML("""
                                <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addBailleurModal">
                                    + Ajouter
                                </button>
                            """
                            ),
                            css_class='form-group col-md-3 mb-0'
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
                            css_class='form-group col-md-12 mb-3'
                        ),
                        Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("statut_contrat"), css_class='form-group col-md-6 mb-0'),
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
                        Column(FloatingField("Administration_beneficiaire"), css_class='form-group col-md-6 col-lg-6 mb-0'),
                        Column(FloatingField("Structure"), css_class='form-group col-md-6 col-lg-6 mb-0'),
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Eléments financiers",
                    Row(
                        Column(FloatingField("Periodicite_Reglement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Nap_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Taxe_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Devise"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Rabattement"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            Field('Soumis_impot'),
                            css_class='form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(
                            Field('Revisitable'),
                            css_class='form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(
                            Field('Visa_controlleur'),
                            css_class='form-group col-md-2 mb-0 pt-3'
                        ),
                        Column(FloatingField("Banque"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("RIB"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Document_RIB"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges_Mensuel"), css_class='form-group col-md-6 mb-0'),
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
                css_class='form-group col-md-6 col-lg-6 mb-0'
            ),
        )
        self.fields['observation'].required = False

# avenants forms
class AvenantsForm(forms.ModelForm):
    class Meta:
        model = Avenants
        fields = (
            "Ref_Avenant",
            "Date_Signature",
            "Date_effet",
            "Modification_apportee",
            "Ancien_bailleur",
            "Nouveau_bailleur",
            "Localite",
            "Montant_TTC_Mensuel_ancien",
            "Montant_TTC_Mensuel_Nouveau",
            "Attestion_domicilliation_bancaire_ancien",
            "Attestion_domicilliation_bancaire_nouveau",
            "Duree_Contrat_Ancien",
            "Duree_Contrat_Nouveau",
        )
        labels = {
            "Ref_Avenant" : "Référence de l'avenant",
            "Date_Signature" : "Date de signature",
            "Date_effet" : "Date de prise d'effet",
            "Modification_apportee" : "Modification apportée",
            "Ancien_bailleur" : "Nom & Prénom de l'ancien bailleur",
            "Nouveau_bailleur" : "Nom & Prénom du nouveau bailleur",
            "Localite" : "Localité",
            "Montant_TTC_Mensuel_ancien" : "Montant Ancien Loyer Mensuel (TTC)",
            "Montant_TTC_Mensuel_Nouveau" : "Montant Nouveau Loyer Mensuel (TTC)",
            "Attestion_domicilliation_bancaire_ancien" : "Ancienne Attestation de domicilliation bancaire",
            "Attestion_domicilliation_bancaire_nouveau" : "Nouvelle Attestation de domicilliation bancaire",
            "Duree_Contrat_Ancien" : "Ancienne Durée Contrat",
            "Duree_Contrat_Nouveau" : "Nouvelle Durée Contrat",
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
                        Column(FloatingField("Ref_Avenant"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_effet"), css_class='form-group col-md-6 mb-0'),
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
                        Column(FloatingField("Modification_apportee"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ancien_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Nouveau_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Localite"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel_ancien"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel_Nouveau"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Attestion_domicilliation_bancaire_ancien"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Attestion_domicilliation_bancaire_nouveau"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat_Ancien"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat_Nouveau"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
        )

# non-mandatement forms
class NonMandatementForm(forms.ModelForm):
    class Meta:
        model = Non_Mandatement
        fields = (
            "Exercice","Loyer_Mensuel","Ref_Attestattion","Date_signature","janvier","fevrier","mars","avril",
            "mai","juin","juillet","aout","septembre","octobre","novembre","decembre","Montant_total_exercice",
            "Visa_budgétaire","Ref_contrat_avenant","Etat",
        )
        labels = {
            "Exercice" : "Exercice",
            "Loyer_Mensuel" : "Loyer Mensuel",
            "Ref_Attestattion" : "Référnce de l'attestation de non mandatement",
            "Date_signature" : "Date de signature",
            "janvier" : "J",
            "fevrier" : "F",
            "mars" : "M",
            "avril" : "A",
            "mai" : "M",
            "juin" : "J",
            "juillet" : "J",
            "aout" : "A",
            "septembre" : "S",
            "octobre" : "O",
            "novembre" : "N",
            "decembre" : "D",
            "Montant_total_exercice" : "Montant total par exercice (Nbre de mois x Loyer Mensuel)",
            "Visa_budgétaire" : "Visa budgétaire / Signature CF ?",
            "Ref_contrat_avenant" : "Reference Contrat / Avenant",
            "Etat" : "Etat",
        }
        widgets = {
          "Date_signature"  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(NonMandatementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations Générales",
                    Row(
                        Column(FloatingField("Exercice"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Loyer_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_Attestattion"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Etat"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Mois non-mandatés",
                    Row(
                        Column("janvier", css_class="col-md-2"),
                        Column("fevrier", css_class="col-md-2"),
                        Column("mars", css_class="col-md-2"),
                        Column("avril", css_class="col-md-2"),
                        Column("mai", css_class="col-md-2"),
                        Column("juin", css_class="col-md-2"),
                        Column("juillet", css_class="col-md-2"),
                        Column("aout", css_class="col-md-2"),
                        Column("septembre", css_class="col-md-2"),
                        Column("octobre", css_class="col-md-2"),
                        Column("novembre", css_class="col-md-2"),
                        Column("decembre", css_class="col-md-2"),
                        css_class="form-row"
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Validation",
                    Row(
                        Column(FloatingField("Montant_total_exercice"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Visa_budgétaire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_contrat_avenant"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
        )
        
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
                        Column(FloatingField("Nom_Prenom"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Contact"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Reference_Grosse"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_prise_effet_grosse"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Reference_certificat_non_effet"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_prise_effet_certificat_non_effet"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
        )

# collectes formset
AvenantsFormSet = inlineformset_factory(
    Collectes, Avenants, form=AvenantsForm,
    extra=1, can_delete=True
)

ImmeublesFormSet = inlineformset_factory(
    Collectes, Immeubles, form=ImmeublesForm,
    extra=1, can_delete=True
)

BailleursFormSet = inlineformset_factory(
    Collectes, Bailleurs, form=BailleursForm,
    extra=1, can_delete=True
)

# Bailleurs formset
NonMandatementFormSet = inlineformset_factory(
    Bailleurs, Non_Mandatement, form=NonMandatementForm,
    extra=1, can_delete=True
)

AyantDroitsFormSet = inlineformset_factory(
    Bailleurs, Ayant_droits, form=AyantDroitsForm,
    extra=1, can_delete=True
)

# occupants formset
OccupantsFormSet = inlineformset_factory(
    Immeubles, Occupants, form=OccupantsForm,
    extra=1, can_delete=True
)

OccupantBureauxFormSet = inlineformset_factory(
    Immeubles, OccupantBureaux, form=OccupantBureauxForm,
    extra=1, max_num=1, can_delete=True
)