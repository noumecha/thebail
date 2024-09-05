# Generated by Django 5.0 on 2024-09-04 11:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0045_locataires_scan_cni_locataires_scan_niu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locataires',
            name='scan_cni',
            field=models.ImageField(blank=True, null=True, upload_to='baux/files/locataire-cni/'),
        ),
        migrations.AlterField(
            model_name='locataires',
            name='scan_niu',
            field=models.ImageField(blank=True, null=True, upload_to='baux/files/locataire-niu/'),
        ),
    ]
