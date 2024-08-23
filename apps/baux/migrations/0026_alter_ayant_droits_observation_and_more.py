# Generated by Django 5.0 on 2024-08-23 02:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0025_remove_occupants_designation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ayant_droits',
            name='Observation',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='dossiers_reglements',
            name='Etat',
            field=models.CharField(choices=[('', 'Choose type of FILES'), ('MANDATE', '1 - facture payée (mandatée)'), ('NON_MANDATE', '2 - facture non-payée (non-mandatée)')], max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='dossiers_reglements',
            name='Observation',
            field=models.TextField(blank=True, null=True),
        ),
    ]