# Generated by Django 5.0 on 2024-08-26 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0036_alter_contrats_imposable'),
    ]

    operations = [
        migrations.AddField(
            model_name='occupants',
            name='Date_Signature_acte_juridique',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
