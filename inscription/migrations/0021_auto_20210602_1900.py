# Generated by Django 3.2.3 on 2021-06-02 17:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0020_auto_20210602_1551'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='numtel_adh',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}')], verbose_name='Numéro téléphone'),
        ),
        migrations.AlterField(
            model_name='adherent',
            name='taille',
            field=models.IntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(100), django.core.validators.MaxValueValidator(210)], verbose_name='Taille en cm'),
        ),
    ]
