# Generated by Django 5.0 on 2024-09-04 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0043_contrats_visa_controlleur'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='avenants',
            name='Banque',
        ),
        migrations.RemoveField(
            model_name='avenants',
            name='Compte_Bancaire',
        ),
        migrations.AddField(
            model_name='avenants',
            name='BanqueAv',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='banques_av', to='baux.banques'),
        ),
        migrations.AddField(
            model_name='avenants',
            name='RIBAv',
            field=models.CharField(max_length=26, null=True),
        ),
    ]
