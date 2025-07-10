from django.db import models
from django import forms

# Create your models here.

MORAL = 1
PHYSIQUE = 2
TYPE_PERSONNE = (
        ('', 'Choose who you are'),
        (str(MORAL), '1 - Personne Morale'),
        (str(PHYSIQUE), '2 - Personne Physique'),
    )
BATI=1
NON_BATI= 2
TYPE_IMMEUBLE = (
        ('', 'Choose type of building'),
        (str(BATI), '1 - Immeuble Bati'),
        (str(NON_BATI), '2 - Immeuble Non-Bati'),
    )   
Nord='N'
Sud ='S'
Ouest ='O'
Est='E'
POSITION_GPS = (
        ('', 'Choose position for GPS'),
        (str(Nord), 'N - Nord'),
        (str(Sud), 'S - Sud'),
        (str(Ouest), 'O - Ouest'),
        (str(Est), 'E - EST'),
    )
LB=1
LP= 2
TYPE_LOCATION = (
        ('', 'Choose type of location'),
        (str(LB), '1 - Location Pour Bureaux'),
        (str(LP), '2 - Location pour logement'),
     )  

Mensuel='M'
trimestriel='T'
Semestriel ='S'
Annuel='A'
PERIODICITE_LOYER = (
        ('', 'Choose DELAY FOR rent payment'),
        (str(Mensuel), '1 - Mensuellement'),
        (str(trimestriel), '2 - Trimestriellement'),
        (str(Semestriel), '3 - Semestriellement'),
        (str(Annuel), '4 - Annuellement'),
    )
ACTIF = 'A'
RESILIE = 'R'
STATUT_CONTRAT = (
    ('', 'Choisir le statut du contrat'),
    (str(ACTIF), '1 - Actif'),
    (str(RESILIE), '2 - Résilié'),
)

M= 'MANDATE'
N = 'NON_MANDATE'
TYPE_DOSSIER = (
        ('', 'Choose type of FILES'),
        (str(M), '1 - facture payée (mandatée)'),
        (str(N), '2 - facture non-payée (non-mandatée)'),
     )  
V = 'VILLA'
D = 'DUPLEX'
A = 'AUTRES'
TYPE_CONSTRUCTION = (
    ('', 'Choisir le type de construction de l\'immeuble'),
    (str(V), '1 - Villa'),
    (str(D), '2 - Duplex '),
    (str(A), '3 - Autres'),
)
C = 'Carrelé'
P = 'Peint'
TYPE_MUR = (
    ('', 'Choisir le type de mur'),
    (str(C), 'Carrelé'),
    (str(P), 'Peint'),
)
MINDCAF = 'MINDCAF'
MINFI = 'MINFI'
MINDEF = 'MINDEF'
PEUT_PAYER = (
    ('', 'Selectionner l\'Administration'),
    (str(MINDCAF), 'MINDCAF'),
    (str(MINFI), 'MINFI'),
    (str(MINDEF), 'MINDEF'),
)
CNI = 'CNI'
PASSEPORT = 'PASSEPORT'
TYPE_IDENTIFICATION = (
    ('', 'Choisir le type d\'identification'),
    (str(CNI), 'CNI'),
    (str(PASSEPORT), 'PASSEPORT'),
)
STATUT_PAY = (
    ('Soumis à l\'impot', 'Soumis à l\'impot'),
    ('Revisitable à la hausse', 'Revisitable à la hausse'),
)
NATURE_CONTRAT = (
    ('Contrat initial', 'Contrat initial'),
    ('Avenant', 'Avenant')
)
DEVISES = (
    ('XAF', 'XAF'),
    ('EUR', 'EUR'),
    ('USD', 'USD'),
    ('XOF', 'XOF'),
    ('YEN', 'YEN')
)

class Exercice(models.Model):
    annee = models.IntegerField(unique=True)
    LibelleFR = models.CharField(max_length=20, null=True)
    date_debut = models.DateField(null=True)
    date_fin = models.DateField(null=True)

    def __str__(self):
        return f"Exercice budgetaire {self.annee}"

class Bailleurs(models.Model):
    Nom_prenom = models.CharField(max_length=50, null=True, blank=True)
    NIU = models.CharField(max_length=20, null=True)
    Reference_doc_identification = models.CharField(max_length=20, null=True, blank=True)
    Registre_commerce = models.CharField(max_length=100, null=True, blank=True)
    Raison_social = models.CharField(max_length=100, null=True, blank=True)
    Date_creationEnt = models.DateField(null=True, blank=True)
    Num_Cni = models.CharField(max_length=50, null=True, blank=True)
    Num_Cni_representant = models.CharField(max_length=50, null=True, blank=True)
    # image fields for saving some stuff
    #Scan_cni = models.ImageField(upload_to=None, height_field=None, width_field=None, max_length=None, null=True)
    Date_delivrance_cni = models.DateField(null=True, blank=True)
    Date_delivrance_cni_representant = models.DateField(null=True, blank=True)
    Type_personne = models.CharField(choices=TYPE_PERSONNE, max_length=1, null=False)
    Type_id_bailleur = models.CharField(choices=TYPE_IDENTIFICATION, max_length=255, null=True, blank=True)
    Type_id_representant = models.CharField(choices=TYPE_IDENTIFICATION, max_length=255, null=True,blank=True)
    NumPassePort = models.CharField(max_length=50, null=True)
    NumPassePort_representant = models.CharField(max_length=50, null=True, blank=True)
    Date_delivrance_PassePort = models.DateField(null=True)
    Date_delivrance_PassePort_representant = models.DateField(null=True, blank=True)
    Nom_Prenom_Representant = models.CharField(max_length=50, null=True, blank=True)
    Telephone = models.CharField(max_length=20, null=True)
    Telephone_representant = models.CharField(max_length=20, null=True, blank=True)
    Adresse = models.CharField(max_length=50, null=True)
    Adresse_representant = models.CharField(max_length=50, null=True, blank=True)
    Observation = models.TextField(blank = True, null= True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        name = self.Nom_prenom if self.Nom_prenom else self.Raison_social
        return f"Bailleur N° {self.id} : {name}"

class Locataires(models.Model):
    Intitule = models.CharField(max_length=50)
    NIU = models.CharField(max_length=20, null=True)
    Nom_Prenom_Representant = models.CharField(max_length=100, null=True)
    Num_Cni = models.CharField(max_length=50, null=True)
    Date_delivrance_cni = models.DateField(null=True)
    Type_personne = models.CharField(choices=TYPE_PERSONNE, max_length=2, null=False)
    Peut_payer = models.CharField(choices=PEUT_PAYER, max_length=255, null=True)
    Observation = models.TextField(blank = True,null= True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"locataire N° {self.id} : {self.Intitule} "

class Administrations (models.Model):
    LibelleFr = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=2, null=True)

    def __str__(self):
        return f"locataire/{self.LibelleFr}"

class Structures (models.Model):
    LibelleFr = models.CharField(max_length=50)
    Administration = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=False, related_name="administration")

    def __str__(self):
        return f"Structure : {self.LibelleFr} "

class Normes (models.Model):
    DesignationFr = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Norme {self.DesignationFr} : {self.AbreviationFr} "

class Pays (models.Model):
    LibelleFR = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)
    Continent = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f"Pays : {self.AbreviationFr} "

class Regions (models.Model):
    Libelle = models.CharField(max_length=50)
    code = models.CharField(max_length=2, null=True)
    AbreviationFr = models.CharField(max_length=20, null=True)

    def __str__(self):
        return f" {self.AbreviationFr} "

class Departements (models.Model):
    LibelleFR = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=4, null=True)
    Region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=False, related_name="region")

    def __str__(self):
        return f"{self.AbreviationFr} "

class Arrondissemements (models.Model):
    LibelleFR = models.CharField(max_length=50)
    code = models.CharField(max_length=9, null=True)
    AbreviationFr = models.CharField(max_length=20, null=True)
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, null=False, related_name="departement")

    def __str__(self):
        return f" {self.AbreviationFr} "

class Localisation (models.Model):
    Quartier = models.CharField(max_length=50,null=True)
    Observation = models.TextField(blank = True,null= True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True, related_name="loca_region")
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, null=True, related_name="loca_departement")
    arrondissement = models.ForeignKey(Arrondissemements, on_delete=models.CASCADE, null=True, related_name="loca_arrondissement")
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, null=True, related_name="etranger")

    def __str__(self):
        return f" {self.arrondissement.departement.Region}/{self.arrondissement.departement}/{self.arrondissement}/{self.Quartier} "

class Immeubles (models.Model):
    Designation = models.CharField(max_length=50)
    Reference_TF = models.CharField(max_length=50,null=True)
    Nom_prenom_proprietaireTF = models.CharField(max_length=50,null=True)
    Element_immeuble = models.CharField(max_length=50,null=True,blank=True)
    #Accessoires = models.CharField(max_length=50,null=True,blank=True)
    Date_signatureTF = models.DateField(null=True)
    Superficie = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Date_Construction = models.DateField(null=True)
    Type_immeuble = models.CharField(choices=TYPE_IMMEUBLE, max_length=1, null=True)
    Type_construction = models.CharField(choices=TYPE_CONSTRUCTION, max_length=255, null=True)
    Type_mur = models.CharField(blank=True, choices=TYPE_MUR, max_length=255, null=True)
    Couleur = models.CharField(max_length=255,null=True,blank=True)
    Nombre_de_pieces = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    Nombre_d_etage = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    Emprise_au_sol = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    Coordonee_gps_latitude = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Coordonee_gps_longitude = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Coordonee_gps_altitude = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Coordonee_gps_Position = models.CharField(choices=POSITION_GPS, max_length=1, null=True) 
    Adresse = models.CharField(max_length=50,null=True)
    Description = models.TextField(blank = True,null= True)
    Localisation = models.ForeignKey(Localisation, on_delete=models.CASCADE, null=True, related_name="localisation")
    Norme = models.ForeignKey(Normes, on_delete=models.CASCADE, null=True, related_name="norme", blank=True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" {self.Designation}/{self.Localisation} "

class Occupants (models.Model):
    Administration_tutelle = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "tutelle")
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="batiment")
    Nom_Prenom = models.CharField(max_length=50,null=True)
    Ref_ActeJuridique = models.CharField(max_length=50,null=True)
    NumCNI = models.CharField(max_length=50,null=True)
    Date_delivrance_CNI = models.DateField(null=True)
    Matricule = models.CharField(max_length=7,null=True)
    Fonction = models.CharField(max_length=50,null=True)
    Telephone = models.CharField(max_length=20,null=True)
    AdresseMail = models.CharField(max_length=20,null=True)
    NumPassePort = models.CharField(max_length=50,null=True)
    Date_Delivrance_PassePort = models.CharField(max_length=50,null=True)
    Date_Signature_acte_juridique = models.CharField(max_length=50,null=True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" logés : {self.Nom_Prenom} "

class Ayant_droits (models.Model):
    Nom_Prenom = models.CharField(max_length=50)
    Num_Cni = models.CharField(max_length=50)
    Date_delivrance_cni = models.DateField(null=True)
    Reference_juridique = models.CharField(max_length=50)
    Observation = models.CharField(max_length=200, null=True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    """ Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=False, related_name= "bailleur")
    """
    Bailleur = models.ManyToManyField(Bailleurs, blank=True)

class Accessoires(models.Model):
    Immeubles = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name='Immeubles')
    Libelle = models.CharField(max_length=255, blank=True, null=True)
    Quantite = models.IntegerField(blank=True, null=True)

class Banques(models.Model):
    codeBanque = models.CharField(max_length=255, blank=True, null=True)
    sigle = models.CharField(max_length=255, blank=True)
    denominationFR = models.CharField(max_length=255, blank=True, null=True)
    denominationUS = models.CharField(max_length=255, blank=True, null=True)
    denominationES = models.CharField(max_length=255, blank=True, null=True)
    siege = models.CharField(max_length=255, blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=255, blank=True, null=True)
    fax = models.CharField(max_length=255, blank=True, null=True)
    webSite = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(max_length=255, blank=True, null=True)
    def __str__(self):
        if self.sigle == "" or len(self.sigle) == 1:
            return f" {self.denominationES} "
        elif self.denominationES == "NULL":
            return f" {self.denominationUS} "
        elif self.denominationUS == "":
            return f" {self.denominationFR} "
        else:
            return f" {self.sigle} "

# type contrat model
class TypeContrats(models.Model):
    libelle = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"Contrat {libelle}"

class Contrats (models.Model):
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "bailleur")
    #Locataire = models.ForeignKey(Locataires, on_delete=models.CASCADE, null=True, related_name= "locataire")
    Immeubles = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name= "immeuble")
    TypeContrat = models.ForeignKey(TypeContrats, on_delete=models.CASCADE, null=True, related_name= "type_contrat")
    Administration_beneficiaire = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "beneficiaire")
    Structure = models.ForeignKey(Structures, on_delete=models.CASCADE, null=True, blank=True, related_name= "structure")
    Superficie_louer = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Duree_Contrat = models.CharField(max_length=10, null=False)
    Signataire = models.CharField(max_length=50, null=False)
    #FonctionSignataire = models.CharField(max_length=50, null=False)
    Devise = models.CharField(choices=DEVISES, max_length=5, null=True)
    Date_Signature = models.DateField(null=True)
    Date_Debut = models.DateField(null=True)
    Ref_contrat = models.CharField(max_length=50, null=True)
    Periodicite_Reglement = models.CharField(choices=PERIODICITE_LOYER, max_length=1, null=True) 
    Montant_Charges_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Taxe_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Rabattement = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Nap_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Banque = models.ForeignKey(Banques, on_delete=models.CASCADE, null=True, related_name="banques")
    RIB = models.CharField(max_length=26, null=True)
    statut_contrat = models.CharField(choices=STATUT_CONTRAT, max_length=1, null=True)
    nature_contrat = models.CharField(max_length=255, choices=NATURE_CONTRAT, null=True)
    Type_location = models.CharField(choices=TYPE_LOCATION, max_length=1, null=True)
    Etat = models.BooleanField(null=True, blank=True)
    observation = models.CharField(max_length=200)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    Soumis_impot = models.BooleanField(null=True, blank=True)
    Revisitable = models.BooleanField(null=True, blank=True)
    Visa_controlleur = models.BooleanField(null=True, blank=True)
    
    def __str__(self):
        return f" Contrat : {self.Ref_contrat}  entre : {self.Bailleur} et  {self.Administration_beneficiaire} " 

class Avenants (models.Model):
    contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=False, related_name= "contrat")
    Duree_Contrat = models.CharField(max_length=10)
    Signataire = models.CharField(max_length=50)
    Date_Signature = models.DateField(null=True)
    Date_Debut = models.DateField(null=True)
    Ref_Avenant = models.CharField(max_length=50)
    Periodicite_Reglement = models.CharField(choices=PERIODICITE_LOYER, max_length=1, null=True) 
    Montant_TTC_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Charges_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Nap_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Banque = models.CharField(max_length=50, null=True, blank=True)
    Compte_Bancaire = models.CharField(max_length=50, null=True, blank=True)
    Type_location = models.CharField(choices=TYPE_LOCATION, max_length=1, null=True) 
    Nom_CF = models.CharField(max_length=50)
    Date_visa_CF = models.DateField(null=True)
    Etat = models.BooleanField(null=True, blank=True)
    observation = models.CharField(max_length=200)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" Avenant : {self.Ref_Avenant}  du  {self.contrat}  " 

class Non_Mandatement (models.Model):
    Avenant = models.ForeignKey(Avenants, on_delete=models.CASCADE, null=True, related_name= "Avenant")
    Contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, related_name= "Contrat")
    Ref_facture = models.CharField(max_length=50)
    Signataire_liquidateur = models.CharField(max_length=50)
    Date_signature = models.DateField(null=True)
    Ref_bonEngagement = models.CharField(max_length=50)
    lieu = models.CharField(max_length=50)
    Date_Effet_debut = models.DateField(null=True)
    Date_Effet_fin = models.DateField(null=True)
    Montant_Brut = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Charges = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Nap = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_reglé = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Etat = models.CharField(choices=TYPE_DOSSIER, max_length=12, null=True) 
    Observation = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now_add=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

  
    def __str__(self):
        return f" Facture : {self.Ref_facture}  du  {self.Etat}  " 