from django import forms
from django.forms import inlineformset_factory, modelformset_factory
from ..models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.bootstrap import InlineRadios, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Button, Field, HTML, LayoutObject
from dal import autocomplete, forward
from django.template.loader import render_to_string
from .nonmandatement_form import *
from .ayantdroit_form import *
from .immeuble_form import *
from .occupant_form import *
from .avenant_form import *

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
                        Column(FloatingField("Intitule"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Peut_payer"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='overflow-hidden form-group col-md-6 mb-0'),  
                        Column(FloatingField("Num_Cni"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_cni"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_personne"), css_class='overflow-hidden form-group col-md-6 mb-0'),  
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
                        Column(FloatingField("Type_localisation"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("pays"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Ville"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Rue"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("region"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("departement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("arrondissement"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        Column(FloatingField("Quartier"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            FloatingField("Observation"),
        )
        self.helper.form_tag = False;self.fields['Observation'].required = False

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
                        Column(FloatingField("Agent_recenseur"), css_class='overflow-hidden form-group col-md-12 mb-0'),
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
                        Column(FloatingField("Immeuble"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                        Column(FloatingField("Description", css_class="overflow-hidden form-group col-md-12 mb-0 mt-1")),
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
                        #Column(FloatingField("Construction"), css_class='overflow-hidden form-group col-md-6 mb-0'),             
                        Column(FloatingField("Emprise_au_sol"), css_class='overflow-hidden form-group col-md-6 mb-0'),             
                        Column(FloatingField("Type_mur"), css_class='overflow-hidden form-group col-md-6 mb-0'),            
                        Column(FloatingField("Couleur"), css_class='color_class overflow-hidden form-group col-md-6 mb-0'),            
                        Column(FloatingField("Type_immeuble"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                        #Column(FloatingField("Situation_de_la_batisse"), css_class='overflow-hidden form-group col-md-6 mb-0'),
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
                Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )
    
class RevetementIntsForm(forms.ModelForm):
    class Meta:
        model = RevetementInts

        fields = ('libelle', 'description')
        labels = {
            'libelle': "Revetement interieur",
            'description': "Description du revetement interieur",
        }
        widgets = {
          'description': forms.Textarea(attrs={'rows':20, 'cols':10}),
        }
        
    def __init__(self, *args, **kwargs):
        super(RevetementIntsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='overflow-hidden form-group col-md-12 mb-0'),
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
                Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='overflow-hidden form-group col-md-12 mb-0'),
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
                    Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),         
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
                    Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-6 mb-0'),
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
                    Column(FloatingField("statut"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    Column(FloatingField("piece"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                    Column(FloatingField("nombre"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                    css_class='form-row'
                ),
                        
            )


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
                # Prepends 
                PrependedText('libelle', 'Contrat MINDCAF-'),
                #Column(FloatingField("libelle"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                Column(FloatingField("description"), css_class='overflow-hidden form-group col-md-12 mb-0'),
                css_class="form-row",
            ),
        )


# Exercice form
class ExercicesForm(forms.ModelForm):
    class Meta:
        model = Exercice
        fields = (
            "annee","LibelleFR","date_debut","date_fin",
        )
        labels = {
            "annee" : "Année d'exercice",
            "LibelleFR" : "Libellé de l'exercice",
            "date_debut" : "Date de debut",
            "date_fin" : "Date de fin",
        }
        widgets = {
            "date_debut"  :  forms.TextInput(attrs={'type': 'date'}),
            "date_fin"  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(ExercicesForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Column(FloatingField("annee"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                Column(FloatingField("LibelleFR"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                Column(FloatingField("date_debut"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                Column(FloatingField("date_fin"), css_class='overflow-hidden form-group col-md-6 mb-0'),
                css_class="form-row",
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