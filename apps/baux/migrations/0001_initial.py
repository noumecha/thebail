# Generated by Django 4.2.13 on 2024-05-16 04:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LibelleFr', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Arrondissemements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LibelleFR', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Avenants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Duree_Contrat', models.CharField(max_length=10)),
                ('Signataire', models.CharField(max_length=50)),
                ('Date_Signature', models.DateField(null=True)),
                ('Date_Debut', models.DateField(null=True)),
                ('Ref_Avenant', models.CharField(max_length=50)),
                ('Periodicite_Reglement', models.CharField(choices=[('', 'Choose DELAY FOR rent payment'), ('M', '1 - Mensuellement'), ('T', '2 - Trimestriellement'), ('S', '3 - Semestriellement'), ('A', '4 - Annuellement')], max_length=1, null=True)),
                ('Montant_TTC_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Charges_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Nap_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Banque', models.CharField(max_length=50)),
                ('Compte_Bancaire', models.CharField(max_length=50)),
                ('Type_location', models.CharField(choices=[('', 'Choose type of location'), ('1', '1 - Location Pour Bureaux'), ('2', '2 - Location pour proprieté')], max_length=1, null=True)),
                ('Nom_CF', models.CharField(max_length=50)),
                ('Date_visa_CF', models.DateField(null=True)),
                ('Etat', models.BooleanField()),
                ('observation', models.CharField(max_length=200)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Bailleurs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom_prenom', models.CharField(max_length=50)),
                ('NIU', models.CharField(max_length=20, null=True)),
                ('Registre_commerce', models.CharField(max_length=100, null=True)),
                ('Num_Cni', models.CharField(max_length=50, null=True)),
                ('Date_delivrance_cni', models.DateField(null=True)),
                ('Type_personne', models.CharField(choices=[('', 'Choose who you are'), ('1', '1 - Personne Morale'), ('2', '2 - Personne Physique')], max_length=1)),
                ('NumPassePort', models.CharField(max_length=50, null=True)),
                ('Date_delivrance_PassePort', models.DateField(null=True)),
                ('Nom_Prenom_Representant', models.CharField(max_length=50, null=True)),
                ('Telephone', models.CharField(max_length=20, null=True)),
                ('Adresse', models.CharField(max_length=50, null=True)),
                ('Observation', models.CharField(max_length=150, null=True)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Contrats',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Duree_Contrat', models.CharField(max_length=10)),
                ('Signataire', models.CharField(max_length=50)),
                ('Date_Signature', models.DateField(null=True)),
                ('Date_Debut', models.DateField(null=True)),
                ('Ref_contrat', models.CharField(max_length=50)),
                ('Periodicite_Reglement', models.CharField(choices=[('', 'Choose DELAY FOR rent payment'), ('M', '1 - Mensuellement'), ('T', '2 - Trimestriellement'), ('S', '3 - Semestriellement'), ('A', '4 - Annuellement')], max_length=1, null=True)),
                ('Montant_TTC_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Charges_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Nap_Mensuel', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Banque', models.CharField(max_length=50)),
                ('Compte_Bancaire', models.CharField(max_length=50)),
                ('Type_location', models.CharField(choices=[('', 'Choose type of location'), ('1', '1 - Location Pour Bureaux'), ('2', '2 - Location pour proprieté')], max_length=1, null=True)),
                ('Nom_CF', models.CharField(max_length=50)),
                ('Date_visa_CF', models.DateField(null=True)),
                ('Etat', models.BooleanField()),
                ('observation', models.CharField(max_length=200)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
                ('Bailleur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bailleur', to='baux.bailleurs')),
            ],
        ),
        migrations.CreateModel(
            name='Exercice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('annee', models.IntegerField(unique=True)),
                ('LibelleFR', models.CharField(max_length=20, null=True)),
                ('date_debut', models.DateField(null=True)),
                ('date_fin', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Immeubles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(max_length=50)),
                ('Reference_TF', models.CharField(max_length=50, null=True)),
                ('Nom_prenom_proprietaireTF', models.CharField(max_length=50, null=True)),
                ('Date_signatureTF', models.DateField(null=True)),
                ('Superficie', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Date_Construction', models.DateField(null=True)),
                ('Type_immeuble', models.CharField(choices=[('', 'Choose type of building'), ('1', '1 - Immeuble Bati'), ('2', '2 - Immeuble Non-Bati')], max_length=1, null=True)),
                ('Coordonee_gps_latitude', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Coordonee_gps_longitude', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Coordonee_gps_altitude', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Coordonee_gps_Position', models.CharField(choices=[('', 'Choose position for GPS'), ('N', 'N - Nord'), ('S', 'S - Sud'), ('O', 'O - Ouest'), ('E', 'E - EST')], max_length=1, null=True)),
                ('Adresse', models.CharField(max_length=50, null=True)),
                ('Description', models.CharField(max_length=250, null=True)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locataires',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Intitule', models.CharField(max_length=50)),
                ('NIU', models.CharField(max_length=20, null=True)),
                ('Nom_Prenom_Representant', models.CharField(max_length=100, null=True)),
                ('Num_Cni', models.CharField(max_length=50, null=True)),
                ('Date_delivrance_cni', models.DateField(null=True)),
                ('Type_personne', models.CharField(choices=[('', 'Choose who you are'), ('1', '1 - Personne Morale'), ('2', '2 - Personne Physique')], max_length=2)),
                ('Observation', models.CharField(max_length=150, null=True)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Normes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DesignationFr', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Pays',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LibelleFR', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
                ('Continent', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Regions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Libelle', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Loges',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Designation', models.CharField(max_length=50)),
                ('Nom_Prenom', models.CharField(max_length=50, null=True)),
                ('Ref_ActeJuridique', models.CharField(max_length=50, null=True)),
                ('NumCNI', models.CharField(max_length=50, null=True)),
                ('Date_delivrance_CNI', models.DateField(null=True)),
                ('Matricule', models.CharField(max_length=7, null=True)),
                ('Fonction', models.CharField(max_length=50, null=True)),
                ('Telephone', models.CharField(max_length=20, null=True)),
                ('AdresseMail', models.CharField(max_length=20, null=True)),
                ('NumPassePort', models.CharField(max_length=50, null=True)),
                ('Date_Delivrance_PassePort', models.CharField(max_length=50, null=True)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
                ('Administration_tutelle', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tutelle', to='baux.administrations')),
                ('Immeuble', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='batiment', to='baux.immeubles')),
            ],
        ),
        migrations.CreateModel(
            name='Localisation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Quartier', models.CharField(max_length=50, null=True)),
                ('Observation', models.CharField(max_length=20, null=True)),
                ('arrondissement', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrondissement', to='baux.arrondissemements')),
                ('pays', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='etranger', to='baux.pays')),
            ],
        ),
        migrations.AddField(
            model_name='immeubles',
            name='Localisation',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='localisation', to='baux.localisation'),
        ),
        migrations.AddField(
            model_name='immeubles',
            name='Norme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='norme', to='baux.normes'),
        ),
        migrations.CreateModel(
            name='Dossiers_Reglements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ref_facture', models.CharField(max_length=50)),
                ('Signataire_liquidateur', models.CharField(max_length=50)),
                ('Date_signature', models.DateField(null=True)),
                ('Ref_bonEngagement', models.CharField(max_length=50)),
                ('lieu', models.CharField(max_length=50)),
                ('Date_Effet_debut', models.DateField(null=True)),
                ('Date_Effet_fin', models.DateField(null=True)),
                ('Montant_Brut', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Charges', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_Nap', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Montant_reglé', models.DecimalField(decimal_places=0, default=0, max_digits=14, null=True)),
                ('Etat', models.CharField(choices=[('', 'Choose type of FILES'), ('MANDATE', '1 - facture paiyée (mandatée)'), ('NON_MANDATE', '2 - facture non-paiyée (non-mandatée)')], max_length=12, null=True)),
                ('Observation', models.CharField(max_length=200)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
                ('Avenant', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Avenant', to='baux.avenants')),
                ('Contrat', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='Contrat', to='baux.contrats')),
            ],
        ),
        migrations.CreateModel(
            name='Departements',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('LibelleFR', models.CharField(max_length=50)),
                ('AbreviationFr', models.CharField(max_length=20, null=True)),
                ('Region', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='region', to='baux.regions')),
            ],
        ),
        migrations.AddField(
            model_name='contrats',
            name='Immeubles',
            field=models.ManyToManyField(blank=True, to='baux.immeubles'),
        ),
        migrations.AddField(
            model_name='contrats',
            name='Locataire',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='locataire', to='baux.locataires'),
        ),
        migrations.CreateModel(
            name='Ayant_droits',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Nom_Prenom', models.CharField(max_length=50)),
                ('Num_Cni', models.CharField(max_length=50)),
                ('Date_delivrance_cni', models.DateField(null=True)),
                ('Reference_juridique', models.CharField(max_length=50)),
                ('Observation', models.CharField(max_length=200)),
                ('Date_creation', models.DateTimeField(auto_now_add=True)),
                ('Date_miseajour', models.DateTimeField(auto_now=True)),
                ('Bailleur', models.ManyToManyField(blank=True, to='baux.bailleurs')),
            ],
        ),
        migrations.AddField(
            model_name='avenants',
            name='contrat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='contrat', to='baux.contrats'),
        ),
        migrations.AddField(
            model_name='arrondissemements',
            name='departement',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departement', to='baux.departements'),
        ),
    ]
