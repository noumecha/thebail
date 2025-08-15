from django import forms
from django.forms import inlineformset_factory
from .models import Recensements, Accessoires, Locataires,TypeContrats, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants
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

        fields = ('Quartier','Observation','arrondissement','pays','region','departement')
        labels = {
            "Quartier": "Nom du Quartier ",
            "arrondissement": "Arrondissement",
            "departement": "Département",
            "region" : "Region",
            "pays": " Pays" ,
            "Observation": "Observation" ,
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
                        Column(FloatingField("pays"), css_class='form-group col-md-6 mb-0'),
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

        fields = ("Administration_tutelle","Date_Signature_acte_juridique","Immeuble","Nom_Prenom","Ref_ActeJuridique","NumCNI","Date_delivrance_CNI","Matricule","Fonction","Telephone","AdresseMail","NumPassePort","Date_Delivrance_PassePort")
        labels = {
            "Administration_tutelle" : "Administration utilisatrice",
            "Immeuble" : "Imeuble",
            "Nom_Prenom" : "Noms et prénoms occupant",
            "Ref_ActeJuridique" : "Référence juridique",
            "Date_Signature_acte_juridique" : "Date Signature de l'acte juridique",
            "NumCNI" : "Numero de CNI",
            "Date_delivrance_CNI" : "Date de délivrance de CNI",
            "Matricule" : "Matricule occupant",
            "Fonction" : "Fonction occupant",
            "Telephone" : "Telephone occupant",
            "AdresseMail" : "Adresse mail occupant",
            "NumPassePort" : "Numero de passeport occupant",
            "Date_Delivrance_PassePort" : "Date de délivrance de passeport du occupant",
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
                        Column(FloatingField("Matricule"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Nom_Prenom"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NumCNI"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NumPassePort"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("AdresseMail"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_CNI"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Delivrance_PassePort"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature_acte_juridique"), css_class='form-group col-md-6 mb-0'),
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
            "Agent_recenseur", "Type_immeuble", "Type_construction", "Type_mur", 
            "Couleur", "Emprise_au_sol", "Description", "Immeuble"
        )

        labels = {
            "Type_immeuble" : "Type immeuble ",
            "Type_construction" : "Type de construction",
            "Type_mur" : "Type de Mur",
            "Couleur" : "Ajouter la couleur",
            "Emprise_au_sol" : "Emprise au sol",
            "Description" : "Autres informations",
            "Immeuble"  : "Immeuble",
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
                        Column(FloatingField("Type_construction"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Emprise_au_sol"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Type_mur"), css_class='form-group col-md-6 mb-0'),            
                        Column(FloatingField("Couleur"), css_class='color_class form-group col-md-6 mb-0'),            
                        Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        self.fields['Description'].required = False   

# immeubles form
class ImmeublesForm(forms.ModelForm):
    class Meta:
        model = Immeubles

        fields = ( "Designation","Reference_TF","Nom_prenom_proprietaireTF","Date_signatureTF",'Element_immeuble',
                   "Superficie","Date_Construction","Coordonee_gps_latitude","Coordonee_gps_longitude","Coordonee_gps_altitude",
                   "Coordonee_gps_Position","Adresse","Localisation","Nombre_de_pieces","Nombre_d_etage", "Norme",)
        labels = {
            "Designation": " Désignation du Bien",
            "Reference_TF": " reference titre foncier (TF)",
            "Element_immeuble" : "Element de l'immeuble",
            "Nom_prenom_proprietaireTF" : "Nom du priopritaire TF",
            "Date_signatureTF" : "Date de signature du TF",
            "Superficie" : "superficie du TF",
            "Date_Construction" : "date de construction",
            "Norme" : "Norme de Cadastrale",
            #"Type_immeuble" : "Type immeuble ",
            #"Type_construction" : "Type de construction",
            #"Type_mur" : "Type de Mur",
            #"Couleur" : "Ajouter la couleur",
            "Nombre_de_pieces" : "Nombre total de pieces",
            "Nombre_d_etage" : "Nombre total d'étages",
            #"Emprise_au_sol" : "Emprise au sol",
            "Coordonee_gps_latitude" : "Coordonne GPS 1 ",
            "Coordonee_gps_longitude": "Coordonne GPS 2 ",
            "Coordonee_gps_altitude": "Coordonne GPS 3 ",
            "Coordonee_gps_Position" : "Coordonne GPS 4 ",
            "Adresse" : "Adresse ou boite postale ",
            #"Description" : "Autres informations",
            "Localisation"  : "localisation",
            #"Norme" : "Norme de l'immeuble (Cadastre)",
        }
        widgets = {
          'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_signatureTF'  :  forms.TextInput(attrs={'type': 'date'}),
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
                        "Caractéristiques du batiment",
                        Row(
                            Column(FloatingField("Designation"), css_class='form-group col-md-6 mb-0'),
                            Column(FloatingField("Date_Construction"), css_class='form-group col-md-6 mb-0'),          
                            Column(FloatingField("Norme"), css_class='form-group col-md-6 mb-0'),  
                            #Column(FloatingField("Type_construction"), css_class='form-group col-md-6 mb-0'),
                            css_class='form-row'
                        ),
                        css_class="line__text border p-2 pt-4"
                    ),
                    css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "Eléments Fonciers",
                    Row(
                        Column(FloatingField("Reference_TF"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Superficie"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),   
                        Column(FloatingField("Nom_prenom_proprietaireTF"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_signatureTF"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Position Géographique",
                    Row(
                        Column(FloatingField("Localisation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Adresse"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
        )
        return helper

    def __init__(self, *args, **kwargs):
        super(ImmeublesForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Caractéristiques du batiment",
                    Row(
                        Column(FloatingField("Designation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Construction"), css_class='form-group col-md-6 mb-0'), 
                        Column(FloatingField("Norme"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Nombre_de_pieces"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Nombre_d_etage"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Element_immeuble"), css_class='form-group col-md-12 mb-0'),               
                        #Column(FloatingField("Accessoires"), css_class='form-group col-md-12 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row (
                Fieldset(
                    "Eléments Fonciers",
                    Row(
                        Column(FloatingField("Reference_TF"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Superficie"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),   
                        Column(FloatingField("Nom_prenom_proprietaireTF"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_signatureTF"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row' 
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Coordonnées GPS",
                    Row(
                        Column(FloatingField("Coordonee_gps_latitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_longitude"), css_class='form-group col-md-6 mb-0'),
                        #Column(FloatingField("Coordonee_gps_altitude"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Coordonee_gps_Position"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
            Row(
                Fieldset(
                    "Position Géographique",
                    Row(
                        Column(FloatingField("Localisation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Adresse"), css_class='form-group col-md-6 mb-0'),
                        css_class='form-row'
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0"
            ),
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

        fields = ( 'Bailleur', 'Immeubles', 'Duree_Contrat', 'Signataire','Date_Signature', 'Date_Debut','Ref_contrat',
            'Periodicite_Reglement','Administration_beneficiaire', 'Montant_Charges_Mensuel','Visa_controlleur','Montant_Nap_Mensuel',
            'Banque', 'RIB', 'Document_RIB', 'Type_location','observation','Soumis_impot','Revisitable', 'statut_contrat', 'TypeContrat', 'nature_contrat',
            "Superficie_louer", 'Montant_Taxe_Mensuel', 'Devise', 'Rabattement', 'Structure', #Locataire
        )
        labels = {
            "Bailleur": "Bailleur ",  
            #"Locataire": "Locataire",  
            "Immeubles": "Imeubles Loués",
            "Superficie_louer" : "Superficie louée",
            "TypeContrat" : "Type du Contrat",
            "Administration_beneficiaire" : "Section / Administration",
            "Structure" : "Chapitre", # Structure  
            "Duree_Contrat":" Durée du Contrat", 
            "Signataire":" Autorité Signataire du contrat",
            "Date_Signature":" Date de Signature du contrat",  
            "Date_Debut":" Date de prise d'effet du contrat ",
            "Ref_contrat":" Réference du contrat",
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
            #'Immeubles' : forms.SelectMultiple(attrs={'class':'select2'}),
            'Date_Debut'  : forms.TextInput(attrs={'type': 'date'}),
            'Date_Signature'  : forms.TextInput(attrs={'type': 'date'}),
            'Soumis_impot' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Revisitable' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Visa_controlleur' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'Structure': autocomplete.ModelSelect2(url='baux:structure_autocomplete'),
            'Administration_beneficiaire': autocomplete.ModelSelect2(url='baux:admins_autocomplete'),
        }
    def __init__(self, *args, **kwargs):
        super(ContratsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Caractéristiques du contrat",
                    Row(
                        Column(FloatingField("TypeContrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("nature_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Superficie_louer"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            # FloatingField("Immeubles"),
                            HTML("""
                                <label for="id_Immeubles">Ajouter un Immeuble</label>
                                <div class="d-flex align-items-center">
                                    {{ form.Immeubles }}
                                    <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addImmeubleModal">
                                        + Ajouter
                                    </button>
                                </div>
                            """),
                            css_class='form-group col-md-12 mb-3'
                        ),
                        Column(FloatingField("Administration_beneficiaire"), css_class='form-group col-md-12 mb-0'),
                        Column(FloatingField("Structure"), css_class='form-group col-md-12 mb-0'),
                        #Column(FloatingField("Locataire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'),
                        Column(
                            # FloatingField("Bailleur"), 
                            HTML(""" 
                                <label for="id_Bailleur">Ajouter un bailleur</label>
                                <div class="d-flex align-items-center">
                                    {{ form.Bailleur }}
                                    <button type="button" class="btn btn-sm btn-outline-primary ms-2" data-bs-toggle="modal" data-bs-target="#addBailleurModal">
                                        + Ajouter
                                    </button>
                                </div>
                            """),
                            css_class='form-group col-md-6 mb-2'
                        ),
                        Column(FloatingField("statut_contrat"), css_class='form-group col-md-6 mb-0'),
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
            Submit(
                "save",
                "Enregistrer",
                css_class="d-grid gap-2 col-4 mx-auto btn btn-primary mb-3"
            )
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
        