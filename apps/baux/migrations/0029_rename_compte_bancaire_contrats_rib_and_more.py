# Generated by Django 5.0 on 2024-08-26 02:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0028_alter_avenants_type_location_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contrats',
            old_name='Compte_Bancaire',
            new_name='RIB',
        ),
        migrations.RemoveField(
            model_name='contrats',
            name='Date_visa_CF',
        ),
        migrations.RemoveField(
            model_name='contrats',
            name='Montant_TTC_Mensuel',
        ),
        migrations.RemoveField(
            model_name='contrats',
            name='Nom_CF',
        ),
    ]