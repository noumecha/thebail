# Generated by Django 5.0 on 2024-08-14 01:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0020_remove_bailleurs_scan_cni'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrats',
            name='Administration_beneficiaire',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='beneficiaire', to='baux.administrations'),
        ),
    ]
