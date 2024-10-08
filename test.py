# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class BauxAccessoires(models.Model):
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(db_column='Libelle', max_length=255, blank=True, null=True)  # Field name made lowercase.
    quantite = models.IntegerField(db_column='Quantite')  # Field name made lowercase.
    immeubles = models.ForeignKey('BauxImmeubles', models.DO_NOTHING, db_column='Immeubles_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_accessoires'


class BauxAdministrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    libellefr = models.CharField(db_column='LibelleFr', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_administrations'


class BauxArrondissemements(models.Model):
    id = models.BigAutoField(primary_key=True)
    libellefr = models.CharField(db_column='LibelleFR', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    departement = models.ForeignKey('BauxDepartements', models.DO_NOTHING)
    code = models.CharField(max_length=9, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_arrondissemements'


class BauxAvenants(models.Model):
    id = models.BigAutoField(primary_key=True)
    duree_contrat = models.CharField(db_column='Duree_Contrat', max_length=10)  # Field name made lowercase.
    signataire = models.CharField(db_column='Signataire', max_length=50)  # Field name made lowercase.
    date_signature = models.DateField(db_column='Date_Signature', blank=True, null=True)  # Field name made lowercase.
    date_debut = models.DateField(db_column='Date_Debut', blank=True, null=True)  # Field name made lowercase.
    ref_avenant = models.CharField(db_column='Ref_Avenant', max_length=50)  # Field name made lowercase.
    periodicite_reglement = models.CharField(db_column='Periodicite_Reglement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    montant_ttc_mensuel = models.DecimalField(db_column='Montant_TTC_Mensuel', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_charges_mensuel = models.DecimalField(db_column='Montant_Charges_Mensuel', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_nap_mensuel = models.DecimalField(db_column='Montant_Nap_Mensuel', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    banque = models.CharField(db_column='Banque', max_length=50)  # Field name made lowercase.
    compte_bancaire = models.CharField(db_column='Compte_Bancaire', max_length=50)  # Field name made lowercase.
    type_location = models.CharField(db_column='Type_location', max_length=1, blank=True, null=True)  # Field name made lowercase.
    nom_cf = models.CharField(db_column='Nom_CF', max_length=50)  # Field name made lowercase.
    date_visa_cf = models.DateField(db_column='Date_visa_CF', blank=True, null=True)  # Field name made lowercase.
    etat = models.IntegerField(db_column='Etat', blank=True, null=True)  # Field name made lowercase.
    observation = models.CharField(max_length=200)
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    contrat = models.ForeignKey('BauxContrats', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'baux_avenants'


class BauxAyantDroits(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_prenom = models.CharField(db_column='Nom_Prenom', max_length=50)  # Field name made lowercase.
    num_cni = models.CharField(db_column='Num_Cni', max_length=50)  # Field name made lowercase.
    date_delivrance_cni = models.DateField(db_column='Date_delivrance_cni', blank=True, null=True)  # Field name made lowercase.
    reference_juridique = models.CharField(db_column='Reference_juridique', max_length=50)  # Field name made lowercase.
    observation = models.CharField(db_column='Observation', max_length=200, blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_ayant_droits'


class BauxAyantDroitsBailleur(models.Model):
    id = models.BigAutoField(primary_key=True)
    ayant_droits = models.ForeignKey(BauxAyantDroits, models.DO_NOTHING)
    bailleurs = models.ForeignKey('BauxBailleurs', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'baux_ayant_droits_bailleur'
        unique_together = (('ayant_droits', 'bailleurs'),)


class BauxBailleurs(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_prenom = models.CharField(db_column='Nom_prenom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    niu = models.CharField(db_column='NIU', max_length=20, blank=True, null=True)  # Field name made lowercase.
    registre_commerce = models.CharField(db_column='Registre_commerce', max_length=100, blank=True, null=True)  # Field name made lowercase.
    num_cni = models.CharField(db_column='Num_Cni', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_cni = models.DateField(db_column='Date_delivrance_cni', blank=True, null=True)  # Field name made lowercase.
    type_personne = models.CharField(db_column='Type_personne', max_length=1)  # Field name made lowercase.
    numpasseport = models.CharField(db_column='NumPassePort', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_passeport = models.DateField(db_column='Date_delivrance_PassePort', blank=True, null=True)  # Field name made lowercase.
    nom_prenom_representant = models.CharField(db_column='Nom_Prenom_Representant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=50, blank=True, null=True)  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    date_creationent = models.DateField(db_column='Date_creationEnt', blank=True, null=True)  # Field name made lowercase.
    raison_social = models.CharField(db_column='Raison_social', max_length=100, blank=True, null=True)  # Field name made lowercase.
    reference_doc_identification = models.CharField(db_column='Reference_doc_identification', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adresse_representant = models.CharField(db_column='Adresse_representant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_passeport_representant = models.DateField(db_column='Date_delivrance_PassePort_representant', blank=True, null=True)  # Field name made lowercase.
    date_delivrance_cni_representant = models.DateField(db_column='Date_delivrance_cni_representant', blank=True, null=True)  # Field name made lowercase.
    numpasseport_representant = models.CharField(db_column='NumPassePort_representant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    num_cni_representant = models.CharField(db_column='Num_Cni_representant', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone_representant = models.CharField(db_column='Telephone_representant', max_length=20, blank=True, null=True)  # Field name made lowercase.
    type_id_bailleur = models.CharField(db_column='Type_id_bailleur', max_length=255, blank=True, null=True)  # Field name made lowercase.
    type_id_representant = models.CharField(db_column='Type_id_representant', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_bailleurs'


class BauxContrats(models.Model):
    id = models.BigAutoField(primary_key=True)
    duree_contrat = models.CharField(db_column='Duree_Contrat', max_length=10)  # Field name made lowercase.
    signataire = models.CharField(db_column='Signataire', max_length=50)  # Field name made lowercase.
    date_signature = models.DateField(db_column='Date_Signature', blank=True, null=True)  # Field name made lowercase.
    date_debut = models.DateField(db_column='Date_Debut', blank=True, null=True)  # Field name made lowercase.
    ref_contrat = models.CharField(db_column='Ref_contrat', max_length=50, blank=True, null=True)  # Field name made lowercase.
    periodicite_reglement = models.CharField(db_column='Periodicite_Reglement', max_length=1, blank=True, null=True)  # Field name made lowercase.
    montant_charges_mensuel = models.DecimalField(db_column='Montant_Charges_Mensuel', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_nap_mensuel = models.DecimalField(db_column='Montant_Nap_Mensuel', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    rib = models.CharField(db_column='RIB', max_length=50, blank=True, null=True)  # Field name made lowercase.
    type_location = models.CharField(db_column='Type_location', max_length=1, blank=True, null=True)  # Field name made lowercase.
    etat = models.IntegerField(db_column='Etat', blank=True, null=True)  # Field name made lowercase.
    observation = models.CharField(max_length=200)
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    bailleur = models.ForeignKey(BauxBailleurs, models.DO_NOTHING, db_column='Bailleur_id', blank=True, null=True)  # Field name made lowercase.
    locataire = models.ForeignKey('BauxLocataires', models.DO_NOTHING, db_column='Locataire_id', blank=True, null=True)  # Field name made lowercase.
    immeubles = models.ForeignKey('BauxImmeubles', models.DO_NOTHING, db_column='Immeubles_id', blank=True, null=True)  # Field name made lowercase.
    administration_beneficiaire = models.ForeignKey(BauxAdministrations, models.DO_NOTHING, db_column='Administration_beneficiaire_id', blank=True, null=True)  # Field name made lowercase.
    imposable = models.CharField(db_column='Imposable', max_length=255, blank=True, null=True)  # Field name made lowercase.
    banque = models.CharField(db_column='Banque', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_contrats'


class BauxDepartements(models.Model):
    id = models.BigAutoField(primary_key=True)
    libellefr = models.CharField(db_column='LibelleFR', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    region = models.ForeignKey('BauxRegions', models.DO_NOTHING, db_column='Region_id')  # Field name made lowercase.
    code = models.CharField(max_length=4, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_departements'


class BauxDossiersReglements(models.Model):
    id = models.BigAutoField(primary_key=True)
    ref_facture = models.CharField(db_column='Ref_facture', max_length=50)  # Field name made lowercase.
    signataire_liquidateur = models.CharField(db_column='Signataire_liquidateur', max_length=50)  # Field name made lowercase.
    date_signature = models.DateField(db_column='Date_signature', blank=True, null=True)  # Field name made lowercase.
    ref_bonengagement = models.CharField(db_column='Ref_bonEngagement', max_length=50)  # Field name made lowercase.
    lieu = models.CharField(max_length=50)
    date_effet_debut = models.DateField(db_column='Date_Effet_debut', blank=True, null=True)  # Field name made lowercase.
    date_effet_fin = models.DateField(db_column='Date_Effet_fin', blank=True, null=True)  # Field name made lowercase.
    montant_brut = models.DecimalField(db_column='Montant_Brut', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_charges = models.DecimalField(db_column='Montant_Charges', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_nap = models.DecimalField(db_column='Montant_Nap', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    montant_reglÚ = models.DecimalField(db_column='Montant_reglÚ', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    etat = models.CharField(db_column='Etat', max_length=12, blank=True, null=True)  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    avenant = models.ForeignKey(BauxAvenants, models.DO_NOTHING, db_column='Avenant_id', blank=True, null=True)  # Field name made lowercase.
    contrat = models.ForeignKey(BauxContrats, models.DO_NOTHING, db_column='Contrat_id', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_dossiers_reglements'


class BauxExercice(models.Model):
    id = models.BigAutoField(primary_key=True)
    annee = models.IntegerField(unique=True)
    libellefr = models.CharField(db_column='LibelleFR', max_length=20, blank=True, null=True)  # Field name made lowercase.
    date_debut = models.DateField(blank=True, null=True)
    date_fin = models.DateField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_exercice'


class BauxImmeubles(models.Model):
    id = models.BigAutoField(primary_key=True)
    designation = models.CharField(db_column='Designation', max_length=50)  # Field name made lowercase.
    reference_tf = models.CharField(db_column='Reference_TF', max_length=50, blank=True, null=True)  # Field name made lowercase.
    nom_prenom_proprietairetf = models.CharField(db_column='Nom_prenom_proprietaireTF', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_signaturetf = models.DateField(db_column='Date_signatureTF', blank=True, null=True)  # Field name made lowercase.
    superficie = models.DecimalField(db_column='Superficie', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    date_construction = models.DateField(db_column='Date_Construction', blank=True, null=True)  # Field name made lowercase.
    type_immeuble = models.CharField(db_column='Type_immeuble', max_length=1, blank=True, null=True)  # Field name made lowercase.
    coordonee_gps_latitude = models.DecimalField(db_column='Coordonee_gps_latitude', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    coordonee_gps_longitude = models.DecimalField(db_column='Coordonee_gps_longitude', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    coordonee_gps_altitude = models.DecimalField(db_column='Coordonee_gps_altitude', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    coordonee_gps_position = models.CharField(db_column='Coordonee_gps_Position', max_length=1, blank=True, null=True)  # Field name made lowercase.
    adresse = models.CharField(db_column='Adresse', max_length=50, blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    localisation = models.ForeignKey('BauxLocalisation', models.DO_NOTHING, db_column='Localisation_id', blank=True, null=True)  # Field name made lowercase.
    norme = models.ForeignKey('BauxNormes', models.DO_NOTHING, db_column='Norme_id', blank=True, null=True)  # Field name made lowercase.
    type_construction = models.CharField(db_column='Type_construction', max_length=255, blank=True, null=True)  # Field name made lowercase.
    emprise_au_sol = models.DecimalField(db_column='Emprise_au_sol', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    nombre_d_etage = models.DecimalField(db_column='Nombre_d_etage', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    nombre_de_pieces = models.DecimalField(db_column='Nombre_de_pieces', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    superficie_louer = models.DecimalField(db_column='Superficie_louer', max_digits=14, decimal_places=0, blank=True, null=True)  # Field name made lowercase.
    type_mur = models.CharField(db_column='Type_mur', max_length=255, blank=True, null=True)  # Field name made lowercase.
    couleur = models.CharField(db_column='Couleur', max_length=255, blank=True, null=True)  # Field name made lowercase.
    element_immeuble = models.CharField(db_column='Element_immeuble', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_immeubles'


class BauxLocalisation(models.Model):
    id = models.BigAutoField(primary_key=True)
    quartier = models.CharField(db_column='Quartier', max_length=50, blank=True, null=True)  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', blank=True, null=True)  # Field name made lowercase.
    arrondissement = models.ForeignKey(BauxArrondissemements, models.DO_NOTHING, blank=True, null=True)
    pays = models.ForeignKey('BauxPays', models.DO_NOTHING, blank=True, null=True)
    departement = models.ForeignKey(BauxDepartements, models.DO_NOTHING, blank=True, null=True)
    region = models.ForeignKey('BauxRegions', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_localisation'


class BauxLocataires(models.Model):
    id = models.BigAutoField(primary_key=True)
    intitule = models.CharField(db_column='Intitule', max_length=50)  # Field name made lowercase.
    niu = models.CharField(db_column='NIU', max_length=20, blank=True, null=True)  # Field name made lowercase.
    nom_prenom_representant = models.CharField(db_column='Nom_Prenom_Representant', max_length=100, blank=True, null=True)  # Field name made lowercase.
    num_cni = models.CharField(db_column='Num_Cni', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_cni = models.DateField(db_column='Date_delivrance_cni', blank=True, null=True)  # Field name made lowercase.
    type_personne = models.CharField(db_column='Type_personne', max_length=2)  # Field name made lowercase.
    observation = models.TextField(db_column='Observation', blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    peut_payer = models.CharField(db_column='Peut_payer', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_locataires'


class BauxNormes(models.Model):
    id = models.BigAutoField(primary_key=True)
    designationfr = models.CharField(db_column='DesignationFr', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_normes'


class BauxOccupants(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom_prenom = models.CharField(db_column='Nom_Prenom', max_length=50, blank=True, null=True)  # Field name made lowercase.
    ref_actejuridique = models.CharField(db_column='Ref_ActeJuridique', max_length=50, blank=True, null=True)  # Field name made lowercase.
    numcni = models.CharField(db_column='NumCNI', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_cni = models.DateField(db_column='Date_delivrance_CNI', blank=True, null=True)  # Field name made lowercase.
    matricule = models.CharField(db_column='Matricule', max_length=7, blank=True, null=True)  # Field name made lowercase.
    fonction = models.CharField(db_column='Fonction', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='Telephone', max_length=20, blank=True, null=True)  # Field name made lowercase.
    adressemail = models.CharField(db_column='AdresseMail', max_length=20, blank=True, null=True)  # Field name made lowercase.
    numpasseport = models.CharField(db_column='NumPassePort', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_delivrance_passeport = models.CharField(db_column='Date_Delivrance_PassePort', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_creation = models.DateTimeField(db_column='Date_creation')  # Field name made lowercase.
    date_miseajour = models.DateTimeField(db_column='Date_miseajour')  # Field name made lowercase.
    administration_tutelle = models.ForeignKey(BauxAdministrations, models.DO_NOTHING, db_column='Administration_tutelle_id', blank=True, null=True)  # Field name made lowercase.
    immeuble = models.ForeignKey(BauxImmeubles, models.DO_NOTHING, db_column='Immeuble_id', blank=True, null=True)  # Field name made lowercase.
    date_signature_acte_juridique = models.CharField(db_column='Date_Signature_acte_juridique', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_occupants'


class BauxPays(models.Model):
    id = models.BigAutoField(primary_key=True)
    libellefr = models.CharField(db_column='LibelleFR', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    continent = models.CharField(db_column='Continent', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'baux_pays'


class BauxRegions(models.Model):
    id = models.BigAutoField(primary_key=True)
    libelle = models.CharField(db_column='Libelle', max_length=50)  # Field name made lowercase.
    abreviationfr = models.CharField(db_column='AbreviationFr', max_length=20, blank=True, null=True)  # Field name made lowercase.
    code = models.CharField(max_length=2, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'baux_regions'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'
