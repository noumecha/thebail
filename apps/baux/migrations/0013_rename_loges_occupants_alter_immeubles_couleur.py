# Generated by Django 5.0 on 2024-08-13 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0012_immeubles_couleur'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Loges',
            new_name='Occupants',
        ),
        migrations.AlterField(
            model_name='immeubles',
            name='Couleur',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
