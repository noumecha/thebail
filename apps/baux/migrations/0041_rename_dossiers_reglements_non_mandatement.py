# Generated by Django 5.0 on 2024-09-02 01:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0040_alter_contrats_banque'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Dossiers_Reglements',
            new_name='Non_Mandatement',
        ),
    ]