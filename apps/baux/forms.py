from django import forms
from django.forms import inlineformset_factory
from .models import Accessoires, Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants,Non_Mandatement,Avenants
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Button, Field

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
          
class BailleursForm(forms.ModelForm):

    class Meta:
        model = Bailleurs

        fields = ( 'Nom_prenom',
                'NIU',
                'Registre_commerce',
                'Num_Cni',
                'Date_delivrance_cni',
                'Type_personne',
                'Raison_social',
                'Reference_doc_identification',
                'Date_creationEnt',
                'NumPassePort',
                'Date_delivrance_PassePort',
                'Nom_Prenom_Representant',
                'Telephone',
                'Adresse',
                'Type_id_bailleur',
                'Num_Cni_representant',
                'Date_delivrance_cni_representant',
                'Type_id_representant',
                'NumPassePort_representant',
                'Date_delivrance_PassePort_representant',
                'Telephone_representant',
                'Adresse_representant',
            )
        labels = {
            "Nom_prenom": " intitulé ou  Nom et prenoms",
            "NIU": "NIU(idientifiant unique DGI)",
            "Reference_doc_identification" : "Reference du document d'identification",
            "Registre_commerce": "Registre du commerce",
            "Nom_Prenom_Representant": " Nom et prenoms du Representant" ,
            "Raison_social" : "Raison social",
            "Date_creationEnt" : "Date de création",
            "Num_Cni": " Numero CNI",
            "Date_delivrance_cni" :"date de delivrance CNI" ,
            "Type_personne": "Type de personne",
            "NumPassePort": " N° passeport",
            "Date_delivrance_PassePort" :"date de delivrance" ,
            "Telephone": "N° Télephone" ,
            "Adresse": "Adresse ou boite postal" ,
            "Num_Cni_representant" : "Numero de CNI du Representant" ,
            "Date_delivrance_cni_representant" : "Date de delivrance CNI Representant" ,
            "Type_id_bailleur" : "Type Identification du bailleur" ,
            "Type_id_representant" : "Type Identification Representant" ,
            "NumPassePort_representant" : "Numero de passeport du Representant" ,
            "Date_delivrance_PassePort_representant" : "Date de delivrance PassePort de Representant" ,
            "Telephone_representant" : "N° Télephone du Representant",
            "Adresse_representant" : "Adresse du Representant",
        }
        widgets = {
            'Date_delivrance_cni'  :  forms.TextInput(attrs={'type': 'date'}),
            'Date_creationEnt'  :  forms.TextInput(attrs={'type': 'date'}),
            'Date_delivrance_PassePort'  :  forms.TextInput(attrs={'type': 'date'}),
            "Date_delivrance_cni_representant" : forms.TextInput(attrs={'type': 'date'}),
            "Date_delivrance_PassePort_representant" : forms.TextInput(attrs={'type': 'date'}),
        }

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
                        Column(FloatingField("Date_creationEnt"), css_class='form-group col-md-6 mb-0 bailleur_date_creation_ent'),
                        Column(FloatingField("Raison_social"), css_class='form-group col-md-6 mb-0 bailleur_raison_social'),
                        Column(FloatingField("NIU"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Reference_doc_identification"), css_class='form-group col-md-6 mb-0 bailleur_niu'),
                        Column(FloatingField("Registre_commerce"), css_class='form-group col-md-6 mb-0 bailleur_registre_commerce'),
                        Column(FloatingField("Adresse"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_id_bailleur"), css_class='form-group col-md-6 mb-0 bailleur_type_id'),  
                        Column(FloatingField("Num_Cni"), css_class='form-group col-md-6 mb-0 bailleur_num_cni'),
                        Column(FloatingField("Date_delivrance_cni"), css_class='form-group col-md-6 mb-0 bailleur_date_deliv_cni'),
                        Column(FloatingField("NumPassePort"), css_class='form-group col-md-6 mb-0 bailleur_num_passeport'),
                        Column(FloatingField("Date_delivrance_PassePort"), css_class='form-group col-md-6 mb-0 bailleur_date_deliv_passeport'),
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
                        Column(FloatingField("Num_Cni_representant"), css_class='form-group col-md-6 mb-0 representant_num_cni'),
                        Column(FloatingField("Date_delivrance_cni_representant"), css_class='form-group col-md-6 mb-0 representant_date_deliv_cni'),
                        Column(FloatingField("NumPassePort_representant"), css_class='form-group col-md-6 mb-0 representant_num_passeport'),
                        Column(FloatingField("Date_delivrance_PassePort_representant"), css_class='form-group col-md-6 mb-0 representant_date_deliv_passeport'),            
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
        self.fields['Num_Cni'].required = False;self.fields['Date_delivrance_cni'].required = False 
        self.fields['NumPassePort'].required = False;self.fields['Date_delivrance_PassePort'].required = False 
        self.fields['Num_Cni_representant'].required = False;self.fields['Date_delivrance_cni_representant'].required = False
        self.fields['NumPassePort_representant'].required = False;self.fields['Date_delivrance_PassePort_representant'].required = False
        self.fields['Telephone_representant'].required = False
        self.fields['Adresse_representant'].required = False;self.fields['Type_id_representant'].required = False


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

class ImmeublesForm(forms.ModelForm):
    class Meta:
        model = Immeubles

        fields = ( "Designation","Reference_TF","Nom_prenom_proprietaireTF","Date_signatureTF","Couleur",'Element_immeuble',
                   "Superficie","Date_Construction","Type_immeuble","Type_construction","Coordonee_gps_latitude","Coordonee_gps_longitude","Coordonee_gps_altitude",
                   "Coordonee_gps_Position","Adresse","Type_mur","Description","Localisation","Norme","Nombre_de_pieces","Nombre_d_etage","Superficie_louer","Emprise_au_sol")
        labels = {
            "Designation": " Désignation du Bien",
            "Reference_TF": " reference titre foncier (TF)",
            "Element_immeuble" : "Element de l'immeuble",
            "Nom_prenom_proprietaireTF" : "Nom du priopritaire TF",
            "Date_signatureTF" : "Date de signature du TF",
            "Superficie" : "superficie du TF",
            "Date_Construction" : "date de construction",
            "Type_immeuble" : "Type immeuble ",
            "Type_construction" : "Type de construction",
            "Type_mur" : "Type de Mur",
            "Couleur" : "Ajouter la couleur",
            "Nombre_de_pieces" : "Nombre total de pieces",
            "Nombre_d_etage" : "Nombre total d'étages",
            "Superficie_louer" : "Superficie louée",
            "Emprise_au_sol" : "Emprise au sol",
            "Coordonee_gps_latitude" : "Coordonne GPS 1 ",
            "Coordonee_gps_longitude": "Coordonne GPS 2 ",
            "Coordonee_gps_altitude": "Coordonne GPS 3 ",
            "Coordonee_gps_Position" : "Coordonne GPS 4 ",
            "Adresse" : "Adresse ou boite postale ",
            "Description" : "Autres informations",
            "Localisation"  : "localisation",
            "Norme" : "Norme de l'immeuble (Cadastre)",
        }
        widgets = {
          'Date_Construction'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_signatureTF'  :  forms.TextInput(attrs={'type': 'date'}),
          'Description' : forms.Textarea(attrs={'rows':4, 'cols':10}),
        }

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
                        Column(FloatingField("Type_construction"), css_class='form-group col-md-6 mb-0'),              
                        Column(FloatingField("Nombre_de_pieces"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Nombre_d_etage"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Superficie_louer"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Emprise_au_sol"), css_class='form-group col-md-6 mb-0'),             
                        Column(FloatingField("Type_mur"), css_class='form-group col-md-6 mb-0'),            
                        Column(FloatingField("Couleur"), css_class='color_class form-group col-md-6 mb-0'),            
                        Column(FloatingField("Norme"), css_class='form-group col-md-6 mb-0'),               
                        Column(FloatingField("Element_immeuble"), css_class='form-group col-md-12 mb-0'),               
                        Column(FloatingField("Accessoires"), css_class='form-group col-md-12 mb-0'),
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
                        Column(FloatingField("Type_immeuble"), css_class='form-group col-md-6 mb-0'),   
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
            FloatingField(
                "Description",
                css_class="mt-1"
            ),
            Submit(
                "save-immeuble",
                "Enregistrer",
                css_class="d-grid gap-2 col-4 mx-auto btn btn-primary mb-3"
            )
        )
        self.helper.form_tag = False;self.fields['Coordonee_gps_latitude'].required = False   
        self.fields['Description'].required = False   
        self.fields['Coordonee_gps_longitude'].required = False; self.fields['Coordonee_gps_altitude'].required = False        
        self.fields['Date_Construction'].required = False;self.fields['Coordonee_gps_Position'].required = False   


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


class ContratsForm(forms.ModelForm):
    class Meta:
        model = Contrats

        fields = ( 'Bailleur', 'Locataire','Immeubles', 'Duree_Contrat', 'Signataire','Date_Signature', 'Date_Debut','Ref_contrat','Periodicite_Reglement', 
                'Administration_beneficiaire', 'Montant_Charges_Mensuel','Visa_controlleur','Montant_Nap_Mensuel', 'Banque', 'RIB', 'Type_location','observation','Soumis_impot','Revisitable' )
        labels = {
            "Bailleur": "Bailleur ",  
            "Locataire": "Locataire",  
            "Immeubles": "Imeubles Loués",
            "Administration_beneficiaire" : "Administration bénéficiaire",  
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
        }
    def __init__(self, *args, **kwargs):
        super(ContratsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Caractéristiques du contrat",
                    Row(
                        Column(FloatingField("Date_Debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Immeubles"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Locataire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Type_location"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Bailleur"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_contrat"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Signataire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Administration_beneficiaire"), css_class='form-group col-md-6 mb-0'),
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
                        Column(FloatingField("Banque"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("RIB"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Periodicite_Reglement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Nap_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges_Mensuel"), css_class='form-group col-md-6 mb-0'),
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
            Submit(
                "save",
                "Enregistrer",
            ),
        )
        self.fields['observation'].required = False

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
            Submit(
                "save",
                "Enregistrer",
                css_class="d-grid gap-2 col-4 mx-auto btn btn-primary mb-3"
            )
        )
        self.fields['Observation'].required = False
        