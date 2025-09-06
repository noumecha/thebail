from django import forms
from django.forms import inlineformset_factory
from .models import TypeConstructions, Recensements, Accessoires, Structures, Administrations, Locataires,TypeContrats, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants
from .models import *
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.layout import HTML
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Button, Field
from dal import autocomplete

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
                'Nom_prenom',
                'NIU',
                'Registre_commerce',
                'Type_personne',
                'Raison_social',
                'Date_creationEnt',
                'Nom_Prenom_Representant',
                'Telephone',
                'Adresse',
                'Type_id_bailleur',
                'Type_id_representant',
                'Telephone_representant',
                'Adresse_representant',
                # new field 
                'Document_identification',
                'Date_delivrance_doc',
                'Date_expiration_doc',
                'Num_doc',
                'Document_identification_rep',
                'Num_doc_representant',
                'Date_delivrance_doc_representant',
                'Date_expiration_doc_representant',
                'Nationalite_bailleur',
            )
        labels = {
            "Nom_prenom": " intitulé ou  Nom et prenoms",
            "NIU": "NIU(idientifiant unique DGI)",
            "Registre_commerce": "Registre du commerce",
            "Nom_Prenom_Representant": " Nom et prenoms du Representant" ,
            "Raison_social" : "Raison social",
            "Date_creationEnt" : "Date de création",
            "Type_personne": "Type de personne",
            "Telephone": "N° Télephone" ,
            "Adresse": "Adresse ou boite postal" ,
            "Type_id_bailleur" : "Type Identification du bailleur" ,
            "Type_id_representant" : "Type Identification Representant" ,
            "Telephone_representant" : "N° Télephone du Representant",
            "Adresse_representant" : "Adresse du Representant",
            # new fields
            "Document_identification" : "Fichier du document",
            "Date_delivrance_doc" : "Date délivrance du document d'identification",
            "Date_expiration_doc" : "Date expiration du docuemnt d'identification",
            "Num_doc" : "Numero du document d'identification",
            "Document_identification_rep" : "Fichier du document d'idenfication du représentant",
            "Num_doc_representant" : "Numeor docuemnt d'identification du représentant",
            "Date_delivrance_doc_representant" : "Date délivrance document d'identification représentant",
            "Date_expiration_doc_representant" : "Date expiration du document d'identification représentant",
            "Nationalite_bailleur" : "Nationalité du bailleur"
        }
        widgets = {
            'Date_delivrance_doc'  :  forms.TextInput(attrs={'type': 'date'}),
            "Date_expiration_doc" : forms.TextInput(attrs={'type': 'date'}),
            'Date_creationEnt'  :  forms.TextInput(attrs={'type': 'date'}),
            "Date_delivrance_doc_representant" : forms.TextInput(attrs={'type': 'date'}),
            "Date_expiration_doc_representant" : forms.TextInput(attrs={'type': 'date'}),
        }

    def partial_form(self):
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_tag = False # remove form tags in the modal
        self.helper.disable_csrf = True # we use default csrf token in the template
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations Bailleur",
                    Row(
                        Column(FloatingField("Type_personne"), css_class='form-group col-md-6 mb-0 bailleur_type_personne'),   
                        Column(FloatingField("Nom_prenom"), css_class='form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        Column(FloatingField("Nationalite_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_creationEnt"), css_class='form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Raison_social"), css_class='form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Reference_doc_identification"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Registre_commerce"), css_class='form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Adresse"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_id_bailleur"), css_class='form-group col-md-6 mb-0 bailleur_type_id'),  
                        Column(FloatingField("Document_identification"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Num_doc"), css_class='form-group col-md-6 mb-0 bailleur_num_cni'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_expiration_doc"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0" 
            )
        )
        return self.helper

    def __init__(self, *args, **kwargs):
        super(BailleursForm, self).__init__(*args, **kwargs)   
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations Bailleur",
                    Row(
                        Column(FloatingField("Type_personne"), css_class='form-group col-md-6 mb-0 bailleur_type_personne'),   
                        Column(FloatingField("Nom_prenom"), css_class='form-group col-md-6 mb-0 bailleur_nom_prenom'),
                        Column(FloatingField("Nationalite_bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_creationEnt"), css_class='form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Raison_social"), css_class='form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Reference_doc_identification"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Registre_commerce"), css_class='form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Adresse"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_id_bailleur"), css_class='form-group col-md-6 mb-0'),  
                        Column(FloatingField("Document_identification"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Num_doc"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_doc"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_expiration_doc"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0" 
            ),
            Row(
                Fieldset(
                    "Informations Representant",
                    Row(
                        Column(FloatingField("Nom_Prenom_Representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_id_representant"), css_class='form-group col-md-6 mb-0 representant_type_id'),
                        Column(FloatingField("Document_identification_rep"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Num_doc_representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_doc_representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_expiration_doc_representant"), css_class='form-group col-md-6 mb-0'),            
                        Column(FloatingField("Telephone_representant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Adresse_representant"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0",
            ),
        )
        self.helper.form_tag = False;self.fields['NIU'].required = False
        self.fields['Registre_commerce'].required = False; self.fields['Nom_Prenom_Representant'].required = False        
        self.fields['Num_doc'].required = False;self.fields['Date_delivrance_doc'].required = False 
        self.fields['Date_expiration_doc'].required = False;self.fields['Date_delivrance_doc_representant'].required = False
        self.fields['Date_expiration_doc_representant'].required = False
        self.fields['Num_doc_representant'].required = False;self.fields['Telephone_representant'].required = False
        self.fields['Adresse_representant'].required = False;self.fields['Type_id_representant'].required = False


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
            "Administration_tutelle","Date_Signature_acte_juridique","Immeuble","Nom_Prenom","Ref_ActeJuridique","Matricule","Fonction","Telephone","NIU","Service"
            #"NumCNI","Date_Delivrance_PassePort","AdresseMail","NumPassePort","Date_delivrance_CNI"
        )
        labels = {
            "Administration_tutelle" : "Administration utilisatrice",
            "Nom_Prenom" : "Noms et prénoms de l'occupant",
            "Matricule" : "Matricule occupant",
            "NIU" : "NIU de l'occupant",
            "Telephone" : "Numéro de téléphone de l'occupant",
            "Service" : "Service de l'occupant",
            "Immeuble" : "Imeuble",
            "Ref_ActeJuridique" : "Référence juridique",
            "Date_Signature_acte_juridique" : "Date Signature de l'acte juridique",
            "Fonction" : "Fonction occupant",
            #"NumCNI" : "Numero de CNI",
            #"Date_delivrance_CNI" : "Date de délivrance de CNI",
            #"AdresseMail" : "Adresse mail occupant",
            #"NumPassePort" : "Numero de passeport occupant",
            #"Date_Delivrance_PassePort" : "Date de délivrance de passeport du occupant",
        }

        widgets = {
            'Date_delivrance_CNI'  :  forms.TextInput(attrs={'type': 'date'}),
            'Date_Delivrance_PassePort'  :  forms.TextInput(attrs={'type': 'date'}),
            'Date_Signature_acte_juridique' : forms.TextInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super(OccupantsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations administratives",
                    Row(
                        Column(FloatingField("Immeuble"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Administration_tutelle"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Service"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row' 
                        """ ,label_class='text-decoration-none' """
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Informations sur l'occupant",
                    Row(
                        Column(FloatingField("Nom_Prenom"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Matricule"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature_acte_juridique"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("NumCNI"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("NumPassePort"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("AdresseMail"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Date_delivrance_CNI"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Date_Delivrance_PassePort"), css_class='form-group col-md-6 mb-0'),
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
# immeubles form
class ImmeublesForm(forms.ModelForm):
    class Meta:
        model = Immeubles

        fields = (
            # idenfification fields
            "Designation","Construction","Date_Construction","Type_location","Nombre_de_pieces", "Norme","Superficie_louer",
            # localisation fields
            "Type_localisation","pays","Ville","Rue","region","departement","arrondissement","Quartier","Coordonee_gps_latitude","Coordonee_gps_longitude",
            "Coordonee_gps_altitude","Coordonee_gps_Position", 
            # etat physique du batiement fields
            "Situation_de_la_batisse","Revetement_interieure","Revetement_exterieure", "observation",
            #"Reference_TF","Nom_prenom_proprietaireTF","Date_signatureTF","Superficie","Nombre_d_etage","Localisation",
        )
        labels = {
            # idenfification labels
            "Designation": " Désignation du Bien",
            "Construction" : "Type de construction",
            "Date_Construction" : "date de construction",
            "Nombre_de_pieces" : "Nombre total de pieces",
            "Superficie_louer" : "Superficie louée",
            "Norme" : "Norme de Cadastrale",
            "Type_location" : "Type de location",
            #"Reference_TF": " reference titre foncier (TF)",
            #"Nom_prenom_proprietaireTF" : "Nom du priopritaire TF",
            #"Date_signatureTF" : "Date de signature du TF",
            "Revetement_interieure" : "Revetement interieure",
            "Revetement_exterieure" : "Revetement exterieure",
            #"Superficie" : "superficie du TF",
            "observation" : "Observation",
            "Situation_de_la_batisse" : "Etat de la batisse",
            #"Type_immeuble" : "Type immeuble ",
            #"Type_construction" : "Type de construction",
            #"Type_mur" : "Type de Mur",
            #"Couleur" : "Ajouter la couleur",
            #"Nombre_d_etage" : "Nombre total d'étages",
            #"Emprise_au_sol" : "Emprise au sol",
            # localisation labels
            "Type_localisation" : "Type de localisation",
            "pays" : "Pays",
            "Ville" : "Ville",
            "Rue" : "Rue",
            "region" : "Région",
            "departement" : "Département",
            "arrondissement" : "Arrondissement",
            "Quartier" : "Quartier",
            "Coordonee_gps_latitude" : "Coordonne GPS 1 ",
            "Coordonee_gps_longitude": "Coordonne GPS 2 ",
            "Coordonee_gps_altitude": "Coordonne GPS 3 ",
            "Coordonee_gps_Position" : "Coordonne GPS 4 ",
            #"Description" : "Autres informations",
            #"Localisation"  : "localisation",
            #"Norme" : "Norme de l'immeuble (Cadastre)",
        }
        widgets = {
          'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
          #'Date_signatureTF'  :  forms.TextInput(attrs={'type': 'date'}),
          #'Description' : forms.Textarea(attrs={'rows':4, 'cols':10}),
        }

    def partial_form(self):
        helper = FormHelper()
        helper.form_method = 'post'
        helper.form_tag = False # remove form tags in the modal
        helper.disable_csrf = True # we use default csrf token in the template
        helper.layout = Layout(
            Row(
                Fieldset(
                        "Identification",
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
                    "Localisation",
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
                        Column(FloatingField("Coordonee_gps_latitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_longitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_altitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_Position"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
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
            Row (
                Fieldset(
                    "Description de la batisse",
                    Row(
                        Column(FloatingField("Situation_de_la_batisse"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            """Row (
                Fieldset(
                    "Eléments Fonciers",
                    Row(
                        #Column(FloatingField("Reference_TF"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Superficie"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),   
                        #Column(FloatingField("Nom_prenom_proprietaireTF"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Date_signatureTF"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),"""
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
                required=False, min_value=1, initial=0, label="",
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
                    Field(f"element_{el.pk}_statut"),
                    Field(f"element_{el.pk}_nombre", css_class="mr-1 w-50"),
                    css_class="p-0 m-0 col-md-4 d-flex align-items-center justify-content-center"
                )
            )
        self.helper =  FormHelper()
        self.helper.layout = Layout(
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
                        #Column(FloatingField("Nombre_d_etage"), css_class='form-group col-md-6 mb-0'), 
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Localisation",
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
                        Column(FloatingField("Coordonee_gps_latitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_longitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_altitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_Position"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
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
            """Row (
                Fieldset(
                    "Eléments Fonciers",
                    Row(
                        #Column(FloatingField("Reference_TF"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Superficie"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),   
                        #Column(FloatingField("Nom_prenom_proprietaireTF"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Date_signatureTF"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="bg-white line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),"""
        )
        self.helper.form_tag = False;self.fields['Coordonee_gps_latitude'].required = False
        self.fields['Coordonee_gps_longitude'].required = False; self.fields['Coordonee_gps_altitude'].required = False        
        self.fields['Date_Construction'].required = False;self.fields['Coordonee_gps_Position'].required = False   

# accessoires forms
class AccessoiresForm(forms.ModelForm):
    class Meta:
        model = Accessoires
        fields = ('Libelle', 'Quantite')
        labels = {
            'Libelle': "Nom accessoires",
            'Quantite': "Quantité",
        }
    def __init__(self, *args, **kwargs):
        super(AccessoiresForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Accessoires",
                    Row(
                        Column(FloatingField("Libelle"), css_class='form-group col-md-4 mb-0'),
                        Column(FloatingField("Quantite"), css_class='form-group col-md-4 mb-0'),
                        Column(Submit("save-accessoire","Ajouter",css_class="d-grid gap-2 col-4 mx-auto btn btn-primary mb-3")),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
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
            "contrat",
            "Duree_Contrat",
            "Signataire",
            "Date_Signature",
            "Date_Debut",
            "Ref_Avenant",
            "Periodicite_Reglement",
            "Montant_TTC_Mensuel",
            "Montant_Charges_Mensuel",
            "Montant_Nap_Mensuel",
            "Banque",
            "Compte_Bancaire",
            "Type_location",
            "Nom_CF",
            "Date_visa_CF",
            "observation",
        )
        labels = {
            "contrat" : "Selectionner le contrat",
            "Duree_Contrat" : "Entrez la durée du contrat",
            "Signataire" : "Entrez le nom du signataire",
            "Date_Signature" : "Selectionner la date de signature",
            "Date_Debut" : "Selectionner la date de debut du contrat",
            "Ref_Avenant" : "Entrez la référence de l'avenant",
            "Periodicite_Reglement" : "Entrez la périodicité de règlement",
            "Montant_TTC_Mensuel" : "Entrez le montant TCC mensuel",
            "Montant_Charges_Mensuel" : "Entrez le montant des charges mensuelles",
            "Montant_Nap_Mensuel" : "Entrez le Net A payer",
            "Banque" : "Entrez le nom de la banque",
            "Compte_Bancaire " : "Entrez le numero du compte bancaire",
            "Type_location" : "Selectionner le type de location",
            "Nom_CF" : "Entrez le nom du controlleur financier",
            "Date_visa_CF" : "Selectionner la date de visa du Controlleur financier",
            "Etat" : "Selectionner l'Etat",
            "observation" : "Observation",
        }
        widgets = {
            "observation" : forms.Textarea(attrs={'rows':4, 'cols':10}),
            "Date_Signature" : forms.TextInput(attrs={'type': 'date'}),
            "Date_Debut" : forms.TextInput(attrs={'type': 'date'}),
            "Date_visa_CF" : forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(AvenantsForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Elémnts du Contrat",
                    Row(
                        Column(FloatingField("contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_Avenant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Eléments CF",
                    Row(
                        Column(FloatingField("Nom_CF"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_visa_CF"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Eléments de règelement",
                    Row(
                        Column(FloatingField("Banque"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Compte_Bancaire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Periodicite_Reglement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Nap_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            FloatingField(
                "observation",
            ),
        )
        self.fields['observation'].required = False

# non-mandatement forms
class Non_MandatementForm(forms.ModelForm):
    class Meta:
        model = Non_Mandatement
        fields = (
            "Avenant",
            "Contrat",
            "Ref_facture",
            "Signataire_liquidateur",
            "Date_signature",
            "Ref_bonEngagement",
            "lieu",
            "Date_Effet_debut",
            "Date_Effet_fin",
            "Montant_Brut",
            "Montant_Charges",
            "Montant_Nap",
            "Montant_reglé",
            "Etat",
            "Observation",
        )
        labels = {
            "Avenant" : "Selectionner l'avenant",
            "Contrat" : "Selectionner le contrat",
            "Ref_facture" : "Saisir la Reférence de la facture",
            "Signataire_liquidateur" : "Signataire liquidateur",
            "Date_signature" : "Date de la signature",
            "Ref_bonEngagement" : "Numero de référecne du bon d'engagement",
            "lieu" : "Saisir le lieu",
            "Date_Effet_debut" : "Date effective de debut",
            "Date_Effet_fin" : "Date effective de fin",
            "Montant_Brut" : "Montant Brut",
            "Montant_Charges" : "Montant des charges",
            "Montant_Nap" : "Montant Net à Payer",
            "Montant_reglé" : "Montant Réglé",
            "Etat" : "Etat",
            "Observation" : "Observation",
        }
        widgets = {
          "Observation" : forms.Textarea(attrs={'rows':4, 'cols':10}),
          "Date_signature"  :  forms.TextInput(attrs={'type': 'date'}),
          "Date_Effet_debut"  :  forms.TextInput(attrs={'type': 'date'}),
          "Date_Effet_fin"  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(Non_MandatementForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Carractéristiques du dossier de règlement",
                    Row(
                        Column(FloatingField("Avenant"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_bonEngagement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Effet_debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Effet_fin"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_facture"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire_liquidateur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("lieu"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Etat"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Eléments financiers",
                    Row(
                        Column(FloatingField("Montant_Brut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Nap"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_reglé"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            FloatingField(
                "Observation",
            ),
        )
        self.fields['Observation'].required = False
        