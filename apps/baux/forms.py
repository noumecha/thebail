from django import forms
from .models import Locataires, Bailleurs,Localisation,Arrondissemements,Pays,Normes,Immeubles,Contrats,Occupants
from crispy_bootstrap5.bootstrap5 import FloatingField
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column, Fieldset, Submit, Button

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
        self.helper.form_tag = False
        self.fields['NIU'].required = False
        self.fields['Num_Cni'].required = False
        self.fields['Date_delivrance_cni'].required = False
          
class BailleursForm(forms.ModelForm):

    class Meta:
        model = Bailleurs

        fields = ( 'Nom_prenom','NIU','Registre_commerce','Num_Cni','Date_delivrance_cni','Type_personne','Raison_social','Reference_doc_identification','Date_creationEnt','NumPassePort','Date_delivrance_PassePort','Nom_Prenom_Representant','Telephone','Adresse')
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
        }
        widgets = {
          'Observation': forms.Textarea(attrs={'rows':4, 'cols':10}),
          'Date_delivrance_cni'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_creationEnt'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_delivrance_PassePort'  :  forms.TextInput(attrs={'type': 'date'}),
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
                        Column(FloatingField("Num_Cni"), css_class='form-group col-md-6 mb-0 bailleur_num_cni'),
                        Column(FloatingField("Date_delivrance_cni"), css_class='form-group col-md-6 mb-0 bailleur_date_deliv_cni'),
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
                        Column(FloatingField("NumPassePort"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_PassePort"), css_class='form-group col-md-6 mb-0'),            
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4",
                ),
                css_class="p-3 pt-0",
            ),
            FloatingField("Adresse"),
            )
        self.helper.form_tag = False;self.fields['NIU'].required = False   
        self.fields['Registre_commerce'].required = False; self.fields['Nom_Prenom_Representant'].required = False        
        self.fields['NumPassePort'].required = False;self.fields['Date_delivrance_PassePort'].required = False   


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
        self.helper.form_tag = False

class OccupantsForm(forms.ModelForm):
    class Meta:
        model = Occupants

        fields = ("Designation","Administration_tutelle","Immeuble","Nom_Prenom","Ref_ActeJuridique","NumCNI","Date_delivrance_CNI","Matricule","Fonction","Telephone","AdresseMail","NumPassePort","Date_Delivrance_PassePort")
        labels = {
            "Designation" : "Désignation",
            "Administration_tutelle" : "Administration utilisatrice",
            "Immeuble" : "Imeuble",
            "Nom_Prenom" : "Noms et prénoms du logé",
            "Ref_ActeJuridique" : "Référence juridique",
            "NumCNI" : "Numero de CNI",
            "Date_delivrance_CNI" : "Date de délivrance de CNI",
            "Matricule" : "Matricule du logé",
            "Fonction" : "Fonction du logé",
            "Telephone" : "Telephone du logé",
            "AdresseMail" : "Adresse mail du logé",
            "NumPassePort" : "Numero de passeport du logé",
            "Date_Delivrance_PassePort" : "Date de délivrance de passeport du logé",
        }

        widgets = {
            'Date_delivrance_CNI'  :  forms.TextInput(attrs={'type': 'date'}),
            'Date_Delivrance_PassePort'  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(OccupantsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Informations administratives",
                    Row(
                        Column(FloatingField("Designation"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Matricule"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Fonction"), css_class='form-group col-md-6 mb-0'),
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
                        Column(FloatingField("Nom_Prenom"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("NumCNI"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Telephone"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("AdresseMail"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_delivrance_CNI"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Delivrance_PassePort"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Ref_ActeJuridique"), css_class='form-group col-md-6 mb-0'),
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
                   'Accessoires',"Superficie","Date_Construction","Type_immeuble","Type_construction","Coordonee_gps_latitude","Coordonee_gps_longitude","Coordonee_gps_altitude",
                   "Coordonee_gps_Position","Adresse","Type_mur","Description","Localisation","Norme","Nombre_de_pieces","Nombre_d_etage","Superficie_louer","Emprise_au_sol")
        labels = {
            "Designation": " Désignation du Bien",
            "Reference_TF": " reference titre foncier (TF)",
            "Element_immeuble" : "Element de l'immeuble",
            "Nom_prenom_proprietaireTF" : "Nom du priopritaire TF",
            "Accessoires" : "Accesoires",
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
        )
        self.helper.form_tag = False;self.fields['Coordonee_gps_latitude'].required = False   
        self.fields['Coordonee_gps_longitude'].required = False; self.fields['Coordonee_gps_altitude'].required = False        
        self.fields['Date_Construction'].required = False;self.fields['Coordonee_gps_Position'].required = False   


class ContratsForm(forms.ModelForm):
    class Meta:
        model = Contrats

        fields = ( 'Bailleur', 'Locataire','Immeubles', 'Duree_Contrat', 'Signataire','Date_Signature', 'Date_Debut','Ref_contrat','Periodicite_Reglement', 
                  'Montant_TTC_Mensuel','Administration_beneficiaire', 'Montant_Charges_Mensuel','Montant_Nap_Mensuel', 'Banque', 'Compte_Bancaire', 'Type_location', 'Nom_CF', 'Date_visa_CF','observation' )
        labels = {
            "Bailleur": "Bailleur ",  
            "Locataire": "Administration Signataire",  
            "Immeubles": "Imeubles Loués",
            "Administration_beneficiaire" : "Administration bénéficiaire",  
            "Duree_Contrat":" Durée du Contrat", 
            "Signataire":" Autorité Signataire du contrat",
            "Date_Signature":" Date de Signature du contrat",  
            "Date_Debut":" Date de prise d'effet du contrat ",
            "Ref_contrat":" Réference du contrat",
            "Periodicite_Reglement":"Periodicite de Reglement ", 
            "Montant_TTC_Mensuel":" Montant TTC du loyer Mensuel",  
            "Montant_Charges_Mensuel":" Montant des Charges Mensuel",
            "Montant_Nap_Mensuel":"Montant NAP LOYER Mensuel",  
            "Banque":" LIBELLE DE LA BANQUE", 
            "Compte_Bancaire":" Numéro du Compte Bancaire",  
            "Type_location":"Type de location", 
            "Nom_CF":" Nom Controleur Financier(CF) Validateur",  
            "Date_visa_CF":"Date du visa du CF ",
            "observation" : 'Observation',
        }
        widgets = {
          'Observation': forms.Textarea(attrs={'rows':4, 'cols':10}),
          #'Immeubles' : forms.SelectMultiple(attrs={'class':'select2'}),
          'Date_visa_CF'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_Debut'  :  forms.TextInput(attrs={'type': 'date'}),
          'Date_Signature'  :  forms.TextInput(attrs={'type': 'date'}),
        }
    def __init__(self, *args, **kwargs):
        super(ContratsForm, self).__init__(*args, **kwargs)
        self.helper =  FormHelper()
        self.helper.layout = Layout(
            Row(
                Fieldset(
                    "Elements du contrat",
                    Row(
                        Column(FloatingField("Immeubles"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Locataire"), css_class='form-group col-md-6 mb-0'),
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
                    "Elements financiers",
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
                    "Durée",
                    Row(
                        Column(FloatingField("Date_Debut"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Date_Signature"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Duree_Contrat"), css_class='form-group col-md-6 mb-0'),
                        css_class="form-row",
                    ),
                    css_class="line__text border p-2 pt-4"
                ),
                css_class="p-3 pt-0",
            ),
            Row(
                Fieldset(
                    "Règlement",
                    Row(
                        Column(FloatingField("Banque"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Compte_Bancaire"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Periodicite_Reglement"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_TTC_Mensuel"), css_class='form-group col-md-6 mb-0'),
                        Column(FloatingField("Montant_Charges_Mensuel"), css_class='form-group col-md-6 mb-0'),
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
                "enregistrer",
                "Enregistrer",
                css_class="d-grid gap-2 col-4 mx-auto btn btn-primary mb-3"
            )
        )
        





    
