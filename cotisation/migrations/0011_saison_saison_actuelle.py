# Generated by Django 3.2.3 on 2021-05-26 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0010_tauxreduction_condition_reduc'),
    ]

    operations = [
        migrations.AddField(
            model_name='saison',
            name='saison_actuelle',
            field=models.BooleanField(default=False),
        ),
    ]