# Generated by Django 5.0 on 2024-08-26 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('baux', '0035_remove_immeubles_accessoires_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contrats',
            name='Imposable',
            field=models.CharField(choices=[("Soumis à l'impot", "Soumis à l'impot"), ('Revisitable à la hausse', 'Revisitable à la hausse')], max_length=255, null=True),
        ),
    ]