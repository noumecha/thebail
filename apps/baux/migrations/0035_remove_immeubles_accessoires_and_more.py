# Generated by Django 5.0 on 2024-08-26 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0034_alter_bailleurs_adresse_representant_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='immeubles',
            name='Accessoires',
        ),
        migrations.AlterField(
            model_name='bailleurs',
            name='Type_id_bailleur',
            field=models.CharField(blank=True, choices=[('', "Choisir le type d'identification"), ('CNI', 'CNI'), ('PASSEPORT', 'PASSEPORT')], max_length=255, null=True),
        ),
    ]
