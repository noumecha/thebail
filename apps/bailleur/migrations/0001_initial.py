# Generated by Django 5.0 on 2024-07-01 00:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locataire', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AyantDroit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom_ayant_droit', models.CharField(max_length=255)),
                ('num_cni_ayant_droit', models.CharField(max_length=255)),
                ('date_delivrance_cni_ayant_droit', models.DateField(auto_now_add=True)),
                ('reference_juridique', models.CharField(max_length=255)),
                ('observation_ayant_droit', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Bailleur',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_prenom_bailleur', models.CharField(max_length=255)),
                ('niu_bailleur', models.CharField(max_length=255)),
                ('registre_commerce_bailleur', models.CharField(max_length=255)),
                ('num_cni_bailleur', models.CharField(max_length=255)),
                ('date_delivrance', models.DateField(auto_now_add=True)),
                ('nom_prenom_responsable', models.CharField(max_length=255)),
                ('telephone_bailleur', models.CharField(max_length=255)),
                ('adresse_bailleur', models.CharField(max_length=255)),
                ('observaiton_bailleur', models.TextField()),
                ('num_cni_ayant_droit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bailleur.ayantdroit')),
                ('type_personne', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locataire.typepersonne')),
            ],
        ),
    ]
