# Generated by Django 3.2.3 on 2021-05-21 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0009_auto_20210521_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='tauxreduction',
            name='condition_reduc',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Conditions à remplir'),
        ),
    ]
