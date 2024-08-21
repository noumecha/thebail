# Generated by Django 5.0 on 2024-08-14 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0021_contrats_administration_beneficiaire'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bailleurs',
            name='Date_creationEnt',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Date_delivrance_cni',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Nom_prenom',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Num_Cni',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Raison_social',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Reference_doc_identification',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Registre_commerce',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
