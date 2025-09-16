from django.db import models
from django import forms
from apps.baux.validators import rib_validator
from django_countries.fields import CountryField
from djmoney.models.fields import MoneyField

# Create your models here.

MORAL = 1
PHYSIQUE = 2
TYPE_PERSONNE = (
        ('', 'Selectionnez le type de personnalité juridique'),
        (str(MORAL), '1 - Personne Morale'),
        (str(PHYSIQUE), '2 - Personne Physique'),
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
    ('', 'Choisir le statut de la batisse'),
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
    ('', 'Choisir le type de location'),
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

STATUT_BAILLEUR = (
    ('Bailleur décédé', 'Bailleur décédé'),
    ('Bailleur vivant', 'Bailleur vivant'),
    ('Ayant droits', 'Ayant-droits légaux et existant(grosse)'),
    ('Administrateur des biens existant', 'Administrateur des biens existant')
)

DEVISES = (
    ("USD", "(USD) United States Dollar"),
    ("EUR", "(EUR) Euro"),
    ("JPY", "(JPY) Japanese Yen"),
    ("GBP", "(GBP) British Pound Sterling"),
    ("AUD", "(AUD) Australian Dollar"),
    ("CAD", "(CAD) Canadian Dollar"),
    ("CHF", "(CHF) Swiss Franc"),
    ("CNY", "(CNY) Chinese Yuan"),
    ("SEK", "(SEK) Swedish Krona"),
    ("NZD", "(NZD) New Zealand Dollar"),
    ("MXN", "(MXN) Mexican Peso"),
    ("SGD", "(SGD) Singapore Dollar"),
    ("HKD", "(HKD) Hong Kong Dollar"),
    ("NOK", "(NOK) Norwegian Krone"),
    ("KRW", "(KRW) South Korean Won"),
    ("TRY", "(TRY) Turkish Lira"),
    ("RUB", "(RUB) Russian Ruble"),
    ("INR", "(INR) Indian Rupee"),
    ("BRL", "(BRL) Brazilian Real"),
    ("ZAR", "(ZAR) South African Rand"),
    ("AED", "(AED) United Arab Emirates Dirham"),
    ("AFN", "(AFN) Afghan Afghani"),
    ("ALL", "(ALL) Albanian Lek"),
    ("AMD", "(AMD) Armenian Dram"),
    ("ANG", "(ANG) Netherlands Antillean Guilder"),
    ("AOA", "(AOA) Angolan Kwanza"),
    ("ARS", "(ARS) Argentine Peso"),
    ("AWG", "(AWG) Aruban Florin"),
    ("AZN", "(AZN) Azerbaijani Manat"),
    ("BAM", "(BAM) Bosnia-Herzegovina Convertible Mark"),
    ("BBD", "(BBD) Barbadian Dollar"),
    ("BDT", "(BDT) Bangladeshi Taka"),
    ("BGN", "(BGN) Bulgarian Lev"),
    ("BHD", "(BHD) Bahraini Dinar"),
    ("BIF", "(BIF) Burundian Franc"),
    ("BMD", "(BMD) Bermudan Dollar"),
    ("BND", "(BND) Brunei Dollar"),
    ("BOB", "(BOB) Bolivian Boliviano"),
    ("BSD", "(BSD) Bahamian Dollar"),
    ("BTN", "(BTN) Bhutanese Ngultrum"),
    ("BWP", "(BWP) Botswanan Pula"),
    ("BYN", "(BYN) Belarusian Ruble"),
    ("BZD", "(BZD) Belize Dollar"),
    ("CDF", "(CDF) Congolese Franc"),
    ("CLP", "(CLP) Chilean Peso"),
    ("COP", "(COP) Colombian Peso"),
    ("CRC", "(CRC) Costa Rican Colón"),
    ("CUP", "(CUP) Cuban Peso"),
    ("CVE", "(CVE) Cape Verdean Escudo"),
    ("CZK", "(CZK) Czech Republic Koruna"),
    ("DJF", "(DJF) Djiboutian Franc"),
    ("DKK", "(DKK) Danish Krone"),
    ("DOP", "(DOP) Dominican Peso"),
    ("DZD", "(DZD) Algerian Dinar"),
    ("EGP", "(EGP) Egyptian Pound"),
    ("ERN", "(ERN) Eritrean Nakfa"),
    ("ETB", "(ETB) Ethiopian Birr"),
    ("FJD", "(FJD) Fijian Dollar"),
    ("FKP", "(FKP) Falkland Islands Pound"),
    ("GEL", "(GEL) Georgian Lari"),
    ("GGP", "(GGP) Guernsey Pound"),
    ("GHS", "(GHS) Ghanaian Cedi"),
    ("GIP", "(GIP) Gibraltar Pound"),
    ("GMD", "(GMD) Gambian Dalasi"),
    ("GNF", "(GNF) Guinean Franc"),
    ("GTQ", "(GTQ) Guatemalan Quetzal"),
    ("GYD", "(GYD) Guyanaese Dollar"),
    ("HNL", "(HNL) Honduran Lempira"),
    ("HRK", "(HRK) Croatian Kuna"),
    ("HTG", "(HTG) Haitian Gourde"),
    ("HUF", "(HUF) Hungarian Forint"),
    ("IDR", "(IDR) Indonesian Rupiah"),
    ("ILS", "(ILS) Israeli New Sheqel"),
    ("IMP", "(IMP) Manx pound"),
    ("IQD", "(IQD) Iraqi Dinar"),
    ("IRR", "(IRR) Iranian Rial"),
    ("ISK", "(ISK) Icelandic Króna"),
    ("JEP", "(JEP) Jersey Pound"),
    ("JMD", "(JMD) Jamaican Dollar"),
    ("JOD", "(JOD) Jordanian Dinar"),
    ("KES", "(KES) Kenyan Shilling"),
    ("KGS", "(KGS) Kyrgystani Som"),
    ("KHR", "(KHR) Cambodian Riel"),
    ("KMF", "(KMF) Comorian Franc"),
    ("KPW", "(KPW) North Korean Won"),
    ("KWD", "(KWD) Kuwaiti Dinar"),
    ("KYD", "(KYD) Cayman Islands Dollar"),
    ("KZT", "(KZT) Kazakhstani Tenge"),
    ("LAK", "(LAK) Laotian Kip"),
    ("LBP", "(LBP) Lebanese Pound"),
    ("LKR", "(LKR) Sri Lankan Rupee"),
    ("LRD", "(LRD) Liberian Dollar"),
    ("LSL", "(LSL) Lesotho Loti"),
    ("LYD", "(LYD) Libyan Dinar"),
    ("MAD", "(MAD) Moroccan Dirham"),
    ("MDL", "(MDL) Moldovan Leu"),
    ("MGA", "(MGA) Malagasy Ariary"),
    ("MKD", "(MKD) Macedonian Denar"),
    ("MMK", "(MMK) Myanma Kyat"),
    ("MNT", "(MNT) Mongolian Tugrik"),
    ("MOP", "(MOP) Macanese Pataca"),
    ("MRU", "(MRU) Mauritanian Ouguiya"),
    ("MUR", "(MUR) Mauritian Rupee"),
    ("MVR", "(MVR) Maldivian Rufiyaa"),
    ("MWK", "(MWK) Malawian Kwacha"),
    ("MYR", "(MYR) Malaysian Ringgit"),
    ("MZN", "(MZN) Mozambican Metical"),
    ("NAD", "(NAD) Namibian Dollar"),
    ("NGN", "(NGN) Nigerian Naira"),
    ("NIO", "(NIO) Nicaraguan Córdoba"),
    ("NPR", "(NPR) Nepalese Rupee"),
    ("OMR", "(OMR) Omani Rial"),
    ("PAB", "(PAB) Panamanian Balboa"),
    ("PEN", "(PEN) Peruvian Nuevo Sol"),
    ("PGK", "(PGK) Papua New Guinean Kina"),
    ("PHP", "(PHP) Philippine Peso"),
    ("PKR", "(PKR) Pakistani Rupee"),
    ("PLN", "(PLN) Polish Zloty"),
    ("PYG", "(PYG) Paraguayan Guarani"),
    ("QAR", "(QAR) Qatari Rial"),
    ("RON", "(RON) Romanian Leu"),
    ("RSD", "(RSD) Serbian Dinar"),
    ("RWF", "(RWF) Rwandan Franc"),
    ("SAR", "(SAR) Saudi Riyal"),
    ("SBD", "(SBD) Solomon Islands Dollar"),
    ("SCR", "(SCR) Seychellois Rupee"),
    ("SDG", "(SDG) Sudanese Pound"),
    ("SHP", "(SHP) Saint Helena Pound"),
    ("SLL", "(SLL) Sierra Leonean Leone"),
    ("SOS", "(SOS) Somali Shilling"),
    ("SRD", "(SRD) Surinamese Dollar"),
    ("SSP", "(SSP) South Sudanese Pound"),
    ("STN", "(STN) São Tomé and Príncipe Dobra"),
    ("SYP", "(SYP) Syrian Pound"),
    ("SZL", "(SZL) Swazi Lilangeni"),
    ("THB", "(THB) Thai Baht"),
    ("TJS", "(TJS) Tajikistani Somoni"),
    ("TMT", "(TMT) Turkmenistani Manat"),
    ("TND", "(TND) Tunisian Dinar"),
    ("TOP", "(TOP) Tongan Paʻanga"),
    ("TTD", "(TTD) Trinidad and Tobago Dollar"),
    ("TWD", "(TWD) New Taiwan Dollar"),
    ("TZS", "(TZS) Tanzanian Shilling"),
    ("UAH", "(UAH) Ukrainian Hryvnia"),
    ("UGX", "(UGX) Ugandan Shilling"),
    ("UYU", "(UYU) Uruguayan Peso"),
    ("UZS", "(UZS) Uzbekistan Som"),
    ("VES", "(VES) Venezuelan Bolívar"),
    ("VND", "(VND) Vietnamese Dong"),
    ("VUV", "(VUV) Vanuatu Vatu"),
    ("WST", "(WST) Samoan Tala"),
    ("XAF", "(XAF) CFA Franc BEAC"),
    ("XCD", "(XCD) East Caribbean Dollar"),
    ("XDR", "(XDR) Special Drawing Rights"),
    ("XOF", "(XOF) CFA Franc BCEAO"),
    ("XPF", "(XPF) CFP Franc"),
    ("YER", "(YER) Yemeni Rial"),
    ("ZMW", "(ZMW) Zambian Kwacha"),
    ("ZWL", "(ZWL) Zimbabwean Dollar"),
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
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

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
    # information d'identifications
    Type_personne = models.CharField(choices=TYPE_PERSONNE, max_length=1, null=False)
    Nom_prenom = models.CharField(max_length=50, null=True, blank=True, unique=True)
    #Nationalite_bailleur = CountryField(blank=True, null=True, blank_label="(Choisir la nationalité)")
    Raison_social = models.CharField(max_length=50, null=True, blank=True, unique=True)
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
    # relations
    # Collecte = models.ForeignKey("Collectes", on_delete=models.CASCADE, null=True, blank=True, related_name="collecte_bailleur")
    #
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

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
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"locataire N° {self.id} : {self.Intitule} "

class Administrations (models.Model):
    LibelleFr = models.CharField(max_length=50)
    AbreviationFr = models.CharField(max_length=20, null=True)
    code = models.CharField(max_length=2, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.LibelleFr}"

class Structures (models.Model):
    LibelleFr = models.CharField(max_length=50)
    Administration = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=False, related_name="administration")
    CodeFr = models.CharField(max_length=50, null=True, blank=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

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
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
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
    libelle = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"
    
# type RevetementInt model
class RevetementInts(models.Model):
    libelle = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# type RevetementExt model
class RevetementExts(models.Model):
    libelle = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"{libelle}"

# Element de description pour un immeuble ex : garage, jardin, piscine etc
class ElementDeDescription(models.Model):
    libelle = models.CharField(max_length=500)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

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
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("immeuble", "element")  # éviter les doublons

    def __str__(self):
        return f"{self.immeuble.Designation} - {self.element.libelle} ({self.nombre})"

# immeubles model
class Immeubles (models.Model):
    # identification
    Designation = models.CharField(max_length=50, unique=True)
    Construction = models.ForeignKey(TypeConstructions, on_delete=models.CASCADE, null=True, related_name="construction")
    Date_Construction = models.DateField(null=True)
    Nombre_de_pieces = models.DecimalField(blank=True, null=True, max_digits=14, decimal_places=0, default=0)
    Superficie_louer = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Norme = models.ForeignKey(Normes, on_delete=models.CASCADE, null=True, related_name="norme", blank=True)
    Type_location = models.CharField(choices=TYPE_LOCATION, max_length=1, null=True)
    # localisation
    Type_localisation = models.CharField(choices=TYPE_LOCALISATION, max_length=1)
    #pays = models.ForeignKey(Pays, on_delete=models.CASCADE, null=True, related_name="immeuble_pays", blank=True)
    pays = CountryField(blank=True, null=True, blank_label="(Choisir le pays)")
    Ville = models.CharField(max_length=50,null=True, blank=True)
    Rue = models.CharField(max_length=50,null=True, blank=True)
    region = models.ForeignKey(Regions, on_delete=models.CASCADE, null=True, related_name="immeuble_region", blank=True)
    departement = models.ForeignKey(Departements, on_delete=models.CASCADE, null=True, related_name="immeuble_departement", blank=True)
    arrondissement = models.ForeignKey(Arrondissemements, on_delete=models.CASCADE, null=True, related_name="immeuble_arrondissement", blank=True)
    Quartier = models.CharField(max_length=50,null=True, blank=True)
    Coordonee_gps = models.CharField(max_length=200, null=True, blank=True)
    # etat physique du batiment
    Situation_de_la_batisse = models.CharField(choices=STATUT_BATISSE, max_length=1, null=True)
    Revetement_interieure = models.ForeignKey(RevetementInts, on_delete=models.CASCADE, null=True, related_name="revetement_interieure")
    Revetement_exterieure = models.ForeignKey(RevetementExts, on_delete=models.CASCADE, null=True, related_name="revetement_exterieure")
    observation = models.CharField(max_length=200, null=True, blank=True)
    # many to many relationship with ElementDeDescription through ImmeubleElement --> description de la batisse
    elements = models.ManyToManyField(ElementDeDescription, through="ImmeubleElement")
    # relationship 
    Collecte = models.ForeignKey("Collectes", on_delete=models.CASCADE, null=True, related_name="collecte_immeuble", blank=True)
    # 
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" {self.Designation} " #/{self.Localisation}

    def nombre_de_recensements(self):
        return self.immeuble_recensement.count()

# Recensements model
class Recensements(models.Model):
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="immeuble_recensement")
    Numero = models.IntegerField()
    # immeuble informations that can be changed 
    # Construction = models.ForeignKey(TypeConstructions, on_delete=models.CASCADE, null=True, related_name="construction")
    Description = models.TextField(blank = True,null= True)
    Etat = models.TextField(blank = True,null= True)
    Agent_recenseur = models.TextField(blank = True,null= True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
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
    Contact = models.IntegerField(max_length=20,null=True)
    Date_initial_acte_occupation = models.CharField(max_length=50,null=True)
    # generic fields 
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="batiment_occ_bureaux")
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f" logés : {self.Service} "

# type occupant résidence
class Occupants (models.Model):
    Nom_Prenom = models.CharField(max_length=50,null=True, unique=True)
    Administration_tutelle = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "tutelle")
    Fonction = models.CharField(max_length=50,null=True)
    Matricule = models.CharField(max_length=7,null=True)
    NIU = models.CharField(max_length=50,null=True)
    Ref_ActeJuridique = models.CharField(max_length=50,null=True)
    Date_Signature_acte_juridique = models.CharField(max_length=50,null=True)
    Telephone = models.CharField(max_length=20,null=True)
    # generic fields 
    Immeuble = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name="batiment_occ_residence")
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f" logés : {self.Nom_Prenom} "

class Ayant_droits (models.Model):
    Nom_Prenom = models.CharField(max_length=50, null=True, blank=True)
    Contact = models.CharField(max_length=50, null=True, blank=True)
    Reference_Grosse = models.CharField(max_length=50, null=True, blank=True)
    Date_prise_effet_grosse = models.CharField(max_length=50,null=True)
    Reference_certificat_non_effet = models.CharField(max_length=50, null=True, blank=True)
    Date_prise_effet_certificat_non_effet = models.CharField(max_length=50,null=True)
    # relations 
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name="bailleur_ayant_droit")
    #
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f" Ayant droit : {self.Nom_Prenom} du bailleur {self.Bailleur} "


# type contrat model
class TypeContrats(models.Model):
    libelle = models.CharField(max_length=500)
    description = models.TextField(blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    # return text
    def __str__(self):
        libelle = self.libelle.upper()
        return f"Contrat {libelle}"

# Piece Collecte -- association table between Collectes and Pieces
class PieceCollectes(models.Model):
    Collecte = models.ForeignKey("Collectes", on_delete=models.CASCADE, related_name="pieces_collectes")
    Piece = models.ForeignKey("Pieces", on_delete=models.CASCADE, related_name="piece")
    statut = models.BooleanField(null=True, blank=True)  # statut de disponibilité oui/non
    nombre = models.PositiveIntegerField(default=0)  # nombre d’éléments collectés
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pièce d'une collecte"
        verbose_name_plural = "Pièces d'un collecte"
        unique_together = ("Collecte", "Piece")  # éviter les doublons

    def __str__(self):
        return f"{self.Collecte.Numero_fiche_de_collecte} - {self.Piece.libelle}"

class Pieces(models.Model):
    libelle = models.CharField(max_length=255, blank=True, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Pièce collectée"
        verbose_name_plural = "Pièces collectées"

    def __str__(self):
        return f" {self.libelle}  "

def upload_piece_file(instance, filename):
    return f"collecte/{instance.piece_collectes.collecte.id}/pieces/{instance.pieces.libelle}/{filename}"

class FichiersPiece(models.Model):
    Collecte_piece = models.ForeignKey(PieceCollectes, on_delete=models.CASCADE, related_name="fichiers")
    fichier = models.FileField(upload_to=upload_piece_file)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fichier de pièce"
        verbose_name_plural = "Fichiers de pièce"

    def __str__(self):
        return f"Fichier {self.fichier.name}"

# Collecte model
class Collectes (models.Model):
    # informations du contrat et sur le collecteur 
    Numero_fiche_de_collecte = models.CharField(max_length=50, null=True)
    Agent_de_collecte = models.TextField(blank = True, null=True)
    Matricule_agent_de_collecte = models.TextField(blank = True, null=True)
    Date_de_collecte = models.CharField(max_length=50,null=True)
    TypeContrat = models.ForeignKey(TypeContrats, on_delete=models.CASCADE, null=True, related_name= "typologie_contrat")
    # informations contrat initial
    Numero_contrat = models.CharField(max_length=50, null=True)
    Date_signature_contrat = models.CharField(max_length=50,null=True)
    Fonction_signataire_contrat = models.CharField(max_length=50,null=True)
    Date_effet_contrat = models.CharField(max_length=50,null=True)
    Regime_fiscal_contrat = models.CharField(max_length=50,null=True)
    Montant_loyer_mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Devise = models.CharField(choices=DEVISES, max_length=5, null=True)
    # avenant informations 
    Existance_avenant = models.BooleanField(verbose_name=('Existence d\'au moins un avenant ?'), choices=EXISTANCE_AVENANT, max_length=1, null=True)
    Existance_visa_budgetaire = models.BooleanField(verbose_name=('Existence du visa budgétaire ?'), choices=EXISTANCE_AVENANT, max_length=1, null=True)
    observation = models.CharField(max_length=200, null=True)
    Periodicite_Reglement = models.CharField(choices=PERIODICITE_LOYER, max_length=1, null=True)
    # many to many relationship with ElementDeDescription through ImmeubleElement --> description de la batisse
    pieces = models.ManyToManyField(Pieces, through="PieceCollectes")
    # relationship : 
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "collecte_bailleur")
    # informations générique
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f" Collecte du  {self.Date_collecte}  du  {self.contrat}  "

# Contrats model
class Contrats (models.Model):
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "bailleur")
    #Locataire = models.ForeignKey(Locataires, on_delete=models.CASCADE, null=True, related_name= "locataire")
    Immeubles = models.ForeignKey(Immeubles, on_delete=models.CASCADE, null=True, related_name= "immeuble")
    TypeContrat = models.ForeignKey(TypeContrats, on_delete=models.CASCADE, null=True, related_name= "type_contrat")
    Administration_beneficiaire = models.ForeignKey(Administrations, on_delete=models.CASCADE, null=True, related_name= "administration_beneficiaire", blank=True)
    Structure = models.ForeignKey(Structures, on_delete=models.CASCADE, null=True, blank=True, related_name= "structure")
    #Superficie_louer = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Duree_Contrat = models.CharField(max_length=10, null=False)
    Signataire = models.CharField(max_length=50, null=False)
    #FonctionSignataire = models.CharField(max_length=50, null=False)
    Devise = models.CharField(choices=DEVISES, max_length=5, null=True)
    Date_Signature = models.DateField(null=True)
    Date_Debut = models.DateField(null=True)
    #Ref_contrat = models.CharField(max_length=50, null=True)
    Periodicite_Reglement = models.CharField(choices=PERIODICITE_LOYER, max_length=1, null=True) 
    Montant_Charges_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Taxe_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Rabattement = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_Nap_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Banque = models.ForeignKey(Banques, on_delete=models.CASCADE, null=True, related_name="banques")
    RIB = models.CharField(max_length=26, null=True)#,validators=[rib_validator]
    Document_RIB = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    statut_contrat = models.CharField(choices=STATUT_CONTRAT, max_length=1, null=True)
    nature_contrat = models.CharField(max_length=255, choices=NATURE_CONTRAT, null=True)
    Type_location = models.CharField(choices=TYPE_LOCATION, max_length=1, null=True)
    Etat = models.BooleanField(null=True, blank=True)
    observation = models.CharField(max_length=200)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)
    Soumis_impot = models.BooleanField(null=True, blank=True)
    Revisitable = models.BooleanField(null=True, blank=True)
    Visa_controlleur = models.BooleanField(null=True, blank=True)
    # fields
    Numero_contrat = models.IntegerField(null=True, blank=True, unique=True)
    
    def __str__(self):
        return f" Contrat N° {self.Numero_contrat} entre : {self.Bailleur} et  {self.Administration_beneficiaire}"  

# Avenants model
class Avenants (models.Model):
    #contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=False, related_name= "contrat")
    collecte = models.ForeignKey(Collectes, on_delete=models.CASCADE, null=True, related_name= "collecte")
    # informations génériques
    Ref_Avenant = models.CharField(max_length=50, unique=True)
    Date_Signature = models.CharField(max_length=50,null=True)
    Date_effet = models.CharField(max_length=50,null=True)
    Modification_apportee = models.TextField(blank = True,null= True)
    Ancien_bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "ancien_bailleur")
    Nouveau_bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "nouveau_bailleur")
    Localite = models.CharField(max_length=50,null=True)
    # informations spécifiques
    Montant_TTC_Mensuel_ancien = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Montant_TTC_Mensuel_Nouveau = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Attestion_domicilliation_bancaire_ancien = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Attestion_domicilliation_bancaire_nouveau = models.ImageField(upload_to='uploads/', height_field=None, width_field=None, max_length=None, blank=True, null=True)
    Duree_Contrat_Ancien = models.CharField(max_length=10, blank = True,null= True)
    Duree_Contrat_Nouveau = models.CharField(max_length=10, blank = True,null= True)
    # informations DB stats
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Avenant : {self.Ref_Avenant} du contrat : {self.collecte}" 

# Non Mandatement model
class Non_Mandatement (models.Model):
    #Avenant = models.ForeignKey(Avenants, on_delete=models.CASCADE, null=True, related_name= "Avenant")
    #Contrat = models.ForeignKey(Contrats, on_delete=models.CASCADE, null=True, related_name= "Contrat")
    Exercice = models.ForeignKey(Exercice, on_delete=models.CASCADE, null=True, related_name= "exercice")
    Loyer_Mensuel = models.DecimalField(null=True, max_digits=14, decimal_places=0, default=0)
    Ref_Attestattion = models.CharField(max_length=50, null=True, blank=True)
    #Date_signature =  models.CharField(max_length=50,null=True)
    # mois non mandatés
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
    Visa_budgétaire = models.BooleanField(verbose_name=('Visa budgétaire / Signature CF ?'), choices=EXISTANCE_AVENANT, max_length=1, null=True)
    Ref_contrat_avenant = models.CharField(max_length=50, null=True, blank=True)
    # relations 
    Bailleur = models.ForeignKey(Bailleurs, on_delete=models.CASCADE, null=True, related_name= "bailleur_non_mandatement")
    # 
    #Etat = models.CharField(choices=TYPE_DOSSIER, max_length=12, null=True)
    Date_creation = models.DateTimeField(auto_now=True)
    Date_miseajour = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Non Mandatement {self.Ref_Attestattion} ({self.Exercice}) "
