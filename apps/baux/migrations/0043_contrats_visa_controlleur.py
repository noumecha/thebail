# Generated by Django 5.0 on 2024-09-02 02:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0042_remove_contrats_imposable_contrats_revisitable_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='contrats',
            name='Visa_controlleur',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
