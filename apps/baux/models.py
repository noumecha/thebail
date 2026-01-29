from django.db import models
from django import forms
from apps.baux.validators import rib_validator
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField
from django.utils import timezone
from django.core.validators import MinValueValidator

# Create your models here.

MORAL = 1
PHYSIQUE = 2
TYPE_PERSONNE = (
        (str(MORAL), 'Personne Morale'),
        (str(PHYSIQUE), 'Personne Physique'),
    )
BATI=1
NON_BATI= 2
TYPE_IMMEUBLE = (
        ('', 'Choisir le type d\'immeuble'),
        (str(BATI), '1 - Immeuble Bati'),
        (str(NON_BATI), '2 - Immeuble Non-Bati'),
    )
Nord='N'
Sud ='S'
Ouest ='O'
Est='E'
POSITION_GPS = (
        ('', 'Choisir la possition GPS'),
        (str(Nord), 'N - Nord'),
        (str(Sud), 'S - Sud'),
        (str(Ouest), 'O - Ouest'),
        (str(Est), 'E - EST'),
    )
STATUT_BATISSE = (
    (str(1), '1 - Bâtisse occupée'),
    (str(2), '2 - Bâtisse non-occupée'),
    (str(3), '3 - Bâtisse en bon état'),
    (str(4), '4 - Bâtisse délabrée et non habitable'),
    (str(5), '5 - Bâtisse délabrée mais habitable'),
    (str(6), '6 - Bâtisse inexistante'),
)

LB=1
LP= 2
DI= 3
DA=4
CO=5
SI=6
TYPE_LOCATION = (
    (str(LB), '1 - Location Pour Bureaux'),
    (str(LP), '2 - Location pour logement'),
    (str(DI), '3 - Domicile'),
    (str(DA), '4 - Domanial'),
    (str(CO), '5 - Conventionné'),
    (str(SI), '6 - Sic'),
)

EX = 1
NA = 2
TYPE_LOCALISATION = (
    ('', 'Choisir le type de localisation'),
    (str(EX), '1 - Représentation diplomatique'),
    (str(NA), '2 - National'),
)

Mensuel='M'
trimestriel='T'
Semestriel ='S'
Annuel='A'
PERIODICITE_LOYER = (
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

STATUT_BAILLEUR = (
    (1, 'Bailleur décédé'),
    (2, 'Ayant-droits légaux et existant(si bailleur décédé)'),
    (3, 'Administrateur des biens existant(si bailleur décédé)'),
)

DEVISES = (
    ("USD", "USD"),
    ("EUR", "EUR"),
    ("JPY", "JPY"),
    ("GBP", "GBP"),
    ("AUD", "AUD"),
    ("CAD", "CAD"),
    ("CHF", "CHF"),
    ("CNY", "CNY"),
    ("SEK", "SEK"),
    ("NZD", "NZD"),
    ("MXN", "MXN"),
    ("SGD", "SGD"),
    ("HKD", "HKD"),
    ("NOK", "NOK"),
    ("KRW", "KRW"),
    ("TRY", "TRY"),
    ("RUB", "RUB"),
    ("INR", "INR"),
    ("BRL", "BRL"),
    ("ZAR", "ZAR"),
    ("AED", "AED"),
    ("AFN", "AFN"),
    ("ALL", "ALL"),
    ("AMD", "AMD"),
    ("ANG", "ANG"),
    ("AOA", "AOA"),
    ("ARS", "ARS"),
    ("AWG", "AWG"),
    ("AZN", "AZN"),
    ("BAM", "BAM"),
    ("BBD", "BBD"),
    ("BDT", "BDT"),
    ("BGN", "BGN"),
    ("BHD", "BHD"),
    ("BIF", "BIF"),
    ("BMD", "BMD"),
    ("BND", "BND"),
    ("BOB", "BOB"),
    ("BSD", "BSD"),
    ("BTN", "BTN"),
    ("BWP", "BWP"),
    ("BYN", "BYN"),
    ("BZD", "BZD"),
    ("CDF", "CDF"),
    ("CLP", "CLP"),
    ("COP", "COP"),
    ("CRC", "CRC"),
    ("CUP", "CUP"),
    ("CVE", "CVE"),
    ("CZK", "CZK"),
    ("DJF", "DJF"),
    ("DKK", "DKK"),
    ("DOP", "DOP"),
    ("DZD", "DZD"),
    ("EGP", "EGP"),
    ("ERN", "ERN"),
    ("ETB", "ETB"),
    ("FJD", "FJD"),
    ("FKP", "FKP"),
    ("GEL", "GEL"),
    ("GGP", "GGP"),
    ("GHS", "GHS"),
    ("GIP", "GIP"),
    ("GMD", "GMD"),
    ("GNF", "GNF"),
    ("GTQ", "GTQ"),
    ("GYD", "GYD"),
    ("HNL", "HNL"),
    ("HRK", "HRK"),
    ("HTG", "HTG"),
    ("HUF", "HUF"),
    ("IDR", "IDR"),
    ("ILS", "ILS"),
    ("IMP", "IMP"),
    ("IQD", "IQD"),
    ("IRR", "IRR"),
    ("ISK", "ISK"),
    ("JEP", "JEP"),
    ("JMD", "JMD"),
    ("JOD", "JOD"),
    ("KES", "KES"),
    ("KGS", "KGS"),
    ("KHR", "KHR"),
    ("KMF", "KMF"),
    ("KPW", "KPW"),
    ("KWD", "KWD"),
    ("KYD", "KYD"),
    ("KZT", "KZT"),
    ("LAK", "LAK"),
    ("LBP", "LBP"),
    ("LKR", "LKR"),
    ("LRD", "LRD"),
    ("LSL", "LSL"),
    ("LYD", "LYD"),
    ("MAD", "MAD"),
    ("MDL", "MDL"),
    ("MGA", "MGA"),
    ("MKD", "MKD"),
    ("MMK", "MMK"),
    ("MNT", "MNT"),
    ("MOP", "MOP"),
    ("MRU", "MRU"),
    ("MUR", "MUR"),
    ("MVR", "MVR"),
    ("MWK", "MWK"),
    ("MYR", "MYR"),
    ("MZN", "MZN"),
    ("NAD", "NAD"),
    ("NGN", "NGN"),
    ("NIO", "NIO"),
    ("NPR", "NPR"),
    ("OMR", "OMR"),
    ("PAB", "PAB"),
    ("PEN", "PEN"),
    ("PGK", "PGK"),
    ("PHP", "PHP"),
    ("PKR", "PKR"),
    ("PLN", "PLN"),
    ("PYG", "PYG"),
    ("QAR", "QAR"),
    ("RON", "RON"),
    ("RSD", "RSD"),
    ("RWF", "RWF"),
    ("SAR", "SAR"),
    ("SBD", "SBD"),
    ("SCR", "SCR"),
    ("SDG", "SDG"),
    ("SHP", "SHP"),
    ("SLL", "SLL"),
    ("SOS", "SOS"),
    ("SRD", "SRD"),
    ("SSP", "SSP"),
    ("STN", "STN"),
    ("SYP", "SYP"),
    ("SZL", "SZL"),
    ("THB", "THB"),
    ("TJS", "TJS"),
    ("TMT", "TMT"),
    ("TND", "TND"),
    ("TOP", "TOP"),
    ("TTD", "TTD"),
    ("TWD", "TWD"),
    ("TZS", "TZS"),
    ("UAH", "UAH"),
    ("UGX", "UGX"),
    ("UYU", "UYU"),
    ("UZS", "UZS"),
    ("VES", "VES"),
    ("VND", "VND"),
    ("VUV", "VUV"),
    ("WST", "WST"),
    ("XAF", "XAF"),
    ("XCD", "XCD"),
    ("XDR", "XDR"),
    ("XOF", "XOF"),
    ("XPF", "XPF"),
    ("YER", "YER"),
    ("ZMW", "ZMW"),
    ("ZWL", "ZWL"),
)
# Existence
EXISTANCE_AVENANT = (
    (True, ('Oui')),
    (False, ('Non'))
)

# exercice model
class Exercice(models.Model):
    annee = models.IntegerField(unique=True)
    LibelleFR = models.CharField(max_length=20, null=True, unique=True)
    date_debut = models.DateField(null=True, blank=True)
    date_fin = models.DateField(null=True, blank=True)
    #
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Exercice budgetaire {self.annee}"

# banque model
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

# bailleur model
class Bailleurs(models.Model):
    # specifics fields
    Type_personne = models.CharField(choices=TYPE_PERSONNE, max_length=1, null=False)
    Nom_prenom = models.CharField(max_length=50, null=True, blank=True, unique=True)
    Raison_social = models.CharField(max_length=200, null=True, blank=True)#, unique=True
    NIU = models.CharField(max_length=14, null=True, blank=True, unique=True)
    Maticule = models.CharField(max_length=14, null=True, blank=True)
    Telephone = models.CharField(max_length=20, null=True)
    Type_id_bailleur = models.CharField(choices=TYPE_IDENTIFICATION, max_length=255, null=True, blank=True)
    Num_doc = models.CharField(max_length=50, null=True)
    Date_delivrance_doc = models.DateField(null=True, blank=True)
    Document_identification = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Nom_Prenom_Representant = models.CharField(max_length=50, null=True, blank=True)
    Telephone_representant = models.CharField(max_length=20, null=True, blank=True)
    Statut_bailleur = models.CharField(choices=STATUT_BAILLEUR, max_length=255, null=True, blank=True)

    # références bancaires
    Banque = models.ForeignKey(Banques, on_delete=models.CASCADE, null=True, related_name="bailleur_banque")
    RIB = models.CharField(max_length=26, null=True)#,validators=[rib_validator]
    Document_RIB = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Intitule_compte = models.CharField(max_length=100, null=True, blank=True)
    #
    Registre_commerce = models.CharField(max_length=100, null=True, blank=True)
    Regime_contribuable = models.CharField(max_length=100, null=True, blank=True)
    Code_centre = models.CharField(max_length=100, null=True, blank=True)
    Raison_social_abr = models.CharField(max_length=100, null=True, blank=True)
    Code_commune = models.CharField(max_length=100, null=True, blank=True)

    # generics fields
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.Nom_prenom == None:
            return f"{self.Raison_social}"
        else:
            return f"{self.Nom_prenom}"

class Locataires(models.Model):
    Intitule = models.CharField(max_length=50)
    NIU = models.CharField(max_length=14, null=True, blank=True)
    Nom_Prenom_Representant = models.CharField(max_length=100, null=True)
    Num_Cni = models.CharField(max_length=50, null=True)
    Date_delivrance_cni = models.DateField(null=True)
    Type_personne = models.CharField(choices=TYPE_PERSONNE, max_length=2, null=False)
    Peut_payer = models.CharField(choices=PEUT_PAYER, max_length=255, null=True)
    Observation = models.TextField(blank = True,null= True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"locataire N° {self.id} : {self.Intitule} "

class Administrations (models.Model):
    LibelleFr = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=2, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.LibelleFr}"

class Structures (models.Model):
    LibelleFr = models.CharField(max_length=50)
    Administration = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=False, related_name="administration")
    CodeFr = models.CharField(max_length=50, null=True, blank=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.LibelleFr}"

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
    Quartier = models.CharField(max_length=50,null=True, blank=True)
    Observation = models.TextField(blank = True,null= True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True, related_name="loca_region", blank=True)
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, null=True, related_name="loca_departement", blank=True)
    arrondissement = models.ForeignKey(Arrondissemements, on_delete=models.CASCADE, null=True, related_name="loca_arrondissement", blank=True)
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, null=True, related_name="etranger", blank=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)
    # new fields
    Type_localisation = models.CharField(choices=TYPE_LOCALISATION, max_length=1, default=NA)
    Ville = models.CharField(max_length=50,null=True, blank=True)
    Rue = models.CharField(max_length=50,null=True, blank=True)

    def __str__(self):
        if self.Type_localisation == '1':
            return f" {self.pays}/{self.Ville}/{self.Rue} "
        else:
            return f" {self.arrondissement.departement.Region}/{self.arrondissement.departement}/{self.arrondissement}/{self.Quartier} "

# type construction model
class TypeConstructions(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# type construction model
class TypeLocations(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# type RevetementInt model
class RevetementInts(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# type RevetementExt model
class RevetementExts(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# statut de la batisse :
class StatutBatisse(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# Element de description pour un immeuble ex : garage, jardin, piscine etc
class ElementDeDescription(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# Immeuble Element -- association table between Immeubles and ElementDeDescription
class ImmeubleElement(models.Model):
    immeuble = models.ForeignKey("Immeubles", on_delete=models.CASCADE, related_name="immeuble_elements")
    element = models.ForeignKey("ElementDeDescription", on_delete=models.CASCADE, related_name="element_immeubles")
    # statut de disponibilité oui/non
    statut = models.BooleanField(null=True, blank=True)  # True = disponible, False = non disponible
    nombre = models.PositiveIntegerField(default=0)  # nombre d’éléments dans l’immeuble
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ("immeuble", "element")  # éviter les doublons

    def __str__(self):
        return f"{self.immeuble.Designation} - {self.element.libelle} ({self.nombre})"

# immeubles model
class Immeubles (models.Model):
    # identification
    Designation = models.CharField(max_length=50, unique=True)
    Construction = models.ForeignKey(TypeConstructions, on_delete=models.CASCADE, null=True, related_name="construction")
    Date_Construction = models.CharField(max_length=50,null=True)
    Nombre_de_pieces = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    Superficie_louer = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Norme = models.ForeignKey(Normes, on_delete=models.CASCADE, null=True, related_name="norme")
    Type_location = models.ForeignKey(TypeLocations, on_delete=models.CASCADE, null=True, related_name="typelocation")
    # localisation
    pays = models.ForeignKey(Pays, on_delete=models.CASCADE, null=True, related_name="immeuble_pays", blank=True)
    Ville = models.CharField(max_length=50,null=True, blank=True)
    Rue = models.CharField(max_length=50,null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True, related_name="immeuble_region", blank=True)
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, null=True, related_name="immeuble_departement", blank=True)
    arrondissement = models.ForeignKey(Arrondissemements, on_delete=models.CASCADE, null=True, related_name="immeuble_arrondissement", blank=True)
    Quartier = models.CharField(max_length=50,null=True, blank=True)
    Coordonee_gps = models.CharField(max_length=200, null=True, blank=True)
    # etat physique du batiment
    Situation_de_la_batisse = models.ForeignKey(StatutBatisse, on_delete=models.CASCADE, null=True, related_name="statut_batisse")
    Revetement_interieure = models.ForeignKey(RevetementInts, on_delete=models.CASCADE, null=True, related_name="revetement_interieure")
    Revetement_exterieure = models.ForeignKey(RevetementExts, on_delete=models.CASCADE, null=True, related_name="revetement_exterieure")
    observation = models.TextField(blank = True,null= True)
    # relationship
    elements = models.ManyToManyField(ElementDeDescription, through="ImmeubleElement")

    #
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" {self.Designation} " #/{self.Localisation}

    def nombre_de_recensements(self):
        return self.immeuble_recensement.count()

class ImmeubleImage(models.Model):
    immeuble = models.ForeignKey(
        Immeubles,
        on_delete=models.CASCADE,
        related_name="immeuble_images"
    )
    image = models.ImageField(upload_to="immeubles/")

    def __str__(self):
        return f"Image de {self.immeuble.Designation}"

# Recensements model
class Recensements(models.Model):
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="immeuble_recensement")
    Numero = models.IntegerField()
    # immeuble informations that can be changed
    # Construction = models.ForeignKey(TypeConstructions, on_delete=models.CASCADE, null=True, related_name="construction")
    Description = models.TextField(blank = True,null= True)
    Etat = models.TextField(blank = True,null= True)
    Agent_recenseur = models.TextField(blank = True,null= True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)
    Type_immeuble = models.CharField(choices=TYPE_IMMEUBLE, max_length=255, null=True)
    Type_mur = models.CharField(blank=True, choices=TYPE_MUR, max_length=255, null=True)
    Couleur = models.CharField(max_length=255,null=True,blank=True)
    Emprise_au_sol = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    # new fieds
    #Situation_de_la_batisse = models.CharField(choices=STATUT_BATISSE, max_length=1, null=True)


    def __str__(self):
        return f"Recensement - {self.Immeuble} - du {self.Date_creation.strftime('%d/%m/%Y')}"

# type occupant bureaux
class OccupantBureaux (models.Model):
    Service = models.ForeignKey(Structures, on_delete=models.CASCADE, null=True, blank=True, related_name= "intitulle_service")
    Administration_correspondante = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "administration_correspondante")
    Fonction = models.CharField(max_length=50,null=True)
    Ref_ActeJuridique_attribution = models.CharField(max_length=50,null=True)
    Contact = models.CharField(max_length=20,null=True, blank=True)
    Date_signature_acte_attribution = models.CharField(max_length=50,null=True)
    # generic fields
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="batiment_occ_bureaux")
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" logés : {self.Service} "

# type occupant résidence
class Occupants (models.Model):
    Nom_Prenom = models.CharField(max_length=50,null=True, unique=True)
    Administration_rattachement = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "tutelle")
    Fonction = models.CharField(max_length=50,null=True)
    Matricule = models.CharField(max_length=7,null=True)
    Ref_ActeJuridique_attribution = models.CharField(max_length=50,null=True)
    Date_Signature_acte_juridique = models.CharField(max_length=50,null=True)
    Telephone = models.CharField(max_length=20,null=True)
    NIU = models.CharField(max_length=50,null=True)
    # generic fields
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="batiment_occ_residence")
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f" logés : {self.Nom_Prenom} "

# Ayant_froit model
class Ayant_droits (models.Model):
    # specific fields
    Nom_Prenom = models.CharField(max_length=200, null=True, blank=True)
    Contact = models.CharField(max_length=200, null=True, blank=True)
    Reference_Grosse = models.CharField(max_length=50, null=True, blank=True)
    Date_delivrance_grosse = models.CharField(max_length=50,null=True)
    Reference_certificat_non_appel = models.CharField(max_length=50, null=True, blank=True)
    Date_delivrance_certificat_non_appel = models.CharField(max_length=50,null=True)

    # relationship
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name="bailleur_ayant_droit")

    # generics fields
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f" Ayant droit : {self.Nom_Prenom} du bailleur {self.Bailleur} "

# type contrat model
class TypeContrats(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# Piece Collecte -- association table between Collectes and Pieces
class PieceCollectes(models.Model):
    Collecte = models.ForeignKey("Collectes", on_delete=models.CASCADE, related_name="pieces_collectes")
    Piece = models.ForeignKey("Pieces", on_delete=models.CASCADE, related_name="piece")
    statut = models.BooleanField(null=True, blank=True)
    nombre = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="immeubles/")
    # timestamps
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Pièce d'une collecte"
        verbose_name_plural = "Pièces d'un collecte"
        unique_together = ("Collecte", "Piece")  # éviter les doublons

    def __str__(self):
        return f"{self.Collecte.Numero_fiche_de_collecte} - {self.Piece.libelle}"

class Pieces(models.Model):
    libelle = models.CharField(max_length=255, blank=True, null=True, unique=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name = "Pièce collectée"
        verbose_name_plural = "Pièces collectées"

    def __str__(self):
        return f" {self.libelle}  "

# model for agent de collecte
class AgentCollecte(models.Model):
    Matricule = models.CharField(max_length=50, null=True, blank=True, unique=True)
    Titre = models.CharField(max_length=50, null=True, blank=True)
    Nom = models.CharField(max_length=50, null=True, blank=True)
    Prenom = models.CharField(max_length=50, null=True, blank=True)
    Nom_jeune_fille = models.CharField(max_length=50, null=True, blank=True)
    Date_naissance = models.CharField(max_length=50, null=True, blank=True)
    Categorie = models.CharField(max_length=50, null=True, blank=True)
    Indice = models.CharField(max_length=50, null=True, blank=True)
    Grade = models.CharField(max_length=50, null=True, blank=True)
    Classe = models.CharField(max_length=50, null=True, blank=True)
    Echelon = models.CharField(max_length=50, null=True, blank=True)
    Chapitre = models.ForeignKey(Structures, on_delete=models.CASCADE, null=True, blank=True, related_name= "agent_service")
    #Chapitre = models.CharField(max_length=50, null=True, blank=True) ---> Chapitre as structure
    Code_fonction = models.CharField(max_length=50, null=True, blank=True)
    Fonction = models.CharField(max_length=50, null=True, blank=True)
    #
    #Date_creation = models.DateTimeField(default=timezone.now)
    #Date_miseajour = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.Nom} {self.Prenom}"

# classe for periodicite_regrelement management
class PeriodiciteReglement(models.Model):
    libelle = models.CharField(max_length=500, unique=True)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return f"{self.libelle}"

# Contrats model
class Contrats (models.Model):
    TypeContrat = models.ForeignKey(TypeContrats, on_delete=models.CASCADE, null=True, related_name= "type_contrat")
    Numero_contrat = models.IntegerField(null=True, blank=True, unique=True)
    Date_Signature_contrat = models.DateField(null=True)
    Fonction_signataire_contrat = models.TextField(null=True, blank=True)
    Date_effet_contrat = models.DateField(null=True)
    Existence_visa_budgétaire = models.BooleanField(null=True, blank=True)
    Duree_Contrat = models.CharField(max_length=10, null=False)
    Tacite_reconduction_contrat = models.BooleanField(null=True, blank=True)
    Regime_fiscal_contrat = models.CharField(max_length=250,null=True)
    Montant_loyer_mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Devise = models.CharField(choices=DEVISES, max_length=5, null=True)
    Existence_avenant = models.BooleanField(null=True, blank=True)
    Periodicite_Reglement = models.ForeignKey(PeriodiciteReglement, on_delete=models.CASCADE, null=True, related_name= "periodicite_reglement_contrat")

    # relationship
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "bailleur")
    Immeubles = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name= "immeuble")
    Administration_beneficiaire = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "administration_beneficiaire", blank=True)
    Structure = models.ForeignKey(Structures, on_delete=models.CASCADE, null=True, blank=True, related_name= "structure")
    Signataire = models.CharField(max_length=50, null=True, blank=True)

    # other
    Fichier_contrat_initial = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Montant_Charges_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Taxe_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Rabattement = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Nap_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Banque = models.ForeignKey(Banques, on_delete=models.CASCADE, null=True, related_name="banques")
    RIB = models.CharField(max_length=26, null=True)
    Document_RIB = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Date_Debut = models.DateField(null=True)
    Date_Signature = models.DateField(null=True)
    statut_contrat = models.CharField(choices=STATUT_CONTRAT, max_length=1, null=True)
    nature_contrat = models.CharField(max_length=255, choices=NATURE_CONTRAT, null=True)
    Type_location = models.CharField(choices=TYPE_LOCATION, max_length=1, null=True)
    Etat = models.BooleanField(null=True, blank=True)
    observation = models.CharField(max_length=200, null=True, blank=True)
    Soumis_impot = models.BooleanField(null=True, blank=True)
    Revisitable = models.BooleanField(null=True, blank=True)
    Visa_controlleur = models.BooleanField(null=True, blank=True)

    # generics fields
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" Contrat N° {self.Numero_contrat} entre : {self.Bailleur} et  {self.Administration_beneficiaire}"

# Avenants model
class Avenants (models.Model):
    # specifics fields
    Ref_Avenant = models.CharField(max_length=50, unique=True)
    Date_Signature = models.CharField(max_length=50,null=True)
    Date_effet = models.CharField(max_length=50,null=True)
    Existence_visa_budgétaire_avenant = models.BooleanField(null=True, blank=True)
    Montant_TTC_Mensuel_ancien = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_TTC_Mensuel_Nouveau = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)

    # relationship
    Ancien_bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "ancien_bailleur")
    Nouveau_bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "nouveau_bailleur")
    contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, blank=True, related_name= "contrat")

    # others fields
    Signataire = models.CharField(max_length=50, null=True, blank=True)
    Modification_apportee = models.TextField(blank = True,null= True)
    Attestion_domicilliation_bancaire_ancien = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Attestion_domicilliation_bancaire_nouveau = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Duree_Contrat_Ancien = models.CharField(max_length=10, blank = True,null= True)
    Duree_Contrat_Nouveau = models.CharField(max_length=10, blank = True,null= True)
    Fichier_avenant = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)

    # generics fields
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Avenant : {self.Ref_Avenant} du contrat : {self.collecte}"

# Non Mandatement model
class Non_Mandatement (models.Model):
    # spefics fields
    Exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, null=True, related_name= "exercice")
    Loyer_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Ref_Attestattion = models.CharField(max_length=50, null=True, blank=True)
    Date_signature =  models.CharField(max_length=50,null=True)
    janvier = models.BooleanField(default=False, verbose_name="Janvier")
    fevrier = models.BooleanField(default=False, verbose_name="Février")
    mars = models.BooleanField(default=False, verbose_name="Mars")
    avril = models.BooleanField(default=False, verbose_name="Avril")
    mai = models.BooleanField(default=False, verbose_name="Mai")
    juin = models.BooleanField(default=False, verbose_name="Juin")
    juillet = models.BooleanField(default=False, verbose_name="Juillet")
    aout = models.BooleanField(default=False, verbose_name="Août")
    septembre = models.BooleanField(default=False, verbose_name="Septembre")
    octobre = models.BooleanField(default=False, verbose_name="Octobre")
    novembre = models.BooleanField(default=False, verbose_name="Novembre")
    decembre = models.BooleanField(default=False, verbose_name="Decembre")
    Montant_total_exercice = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Visa_budgétaire = models.BooleanField(null=True, blank=True)
    Ref_contrat_avenant = models.CharField(max_length=50, null=True, blank=True)

    # others
    Fichier_nonmandatement = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)

    # relationship
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "bailleur_non_mandatement")

    # generics fields
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def mois_status(self):
        """Return a list of (month_name, value) for easy template loop"""
        months = [
            'janvier', 'fevrier', 'mars', 'avril', 'mai', 'juin',
            'juillet', 'aout', 'septembre', 'octobre', 'novembre', 'decembre'
        ]
        return [(m, getattr(self, m)) for m in months]

    def __str__(self):
        return f"Non Mandatement {self.Ref_Attestattion} ({self.Exercice}) "

# Collecte model
class Collectes (models.Model):
    # specific fields for collecte
    Numero_fiche_de_collecte = models.CharField(max_length=50, null=True, unique=True)
    Date_de_collecte = models.CharField(max_length=50,null=True)
    observation_generale = models.TextField(blank = True,null= True)
    signature_responsable = models.CharField(max_length=200, null=True, blank=True)
    # relationships :
    pieces = models.ManyToManyField(Pieces, through="PieceCollectes")
    Contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, related_name="collecte_contrat")
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="collecte_immeuble")
    Agent = models.ForeignKey(AgentCollecte, on_delete=models.CASCADE, null=True, related_name= "collecte_agent")
    # generics informations :
    Date_creation = models.DateTimeField(default=timezone.now)
    Date_miseajour = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f" Collecte du  {self.Date_collecte}  du  {self.contrat}  "
