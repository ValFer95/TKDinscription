# Generated by Django 3.2.3 on 2021-07-04 12:42

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0021_auto_20210602_1900'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='numtel_adh',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}', message='Saisissez un numéro de téléphone valide.')], verbose_name='Numéro téléphone'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='numtel_contact1',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator('[0-9]{10}', message='Saisissez un numéro de téléphone valide pour le contact principal.')], verbose_name='Numéro téléphone 1'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='numtel_contact2',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}', message='Saisissez un numéro de téléphone valide pour le contact 2.')], verbose_name='Numéro téléphone 2'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='numtel_contact3',
            field=models.CharField(blank=True, max_length=10, null=True, validators=[django.core.validators.RegexValidator('[0-9]{10}', message='Saisissez un numéro de téléphone valide pour le contact 3.')], verbose_name='Numéro téléphone 3'),
        ),
    ]
