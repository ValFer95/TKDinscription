# Generated by Django 3.2.3 on 2021-05-27 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0009_remove_categoriecombat_age'),
    ]

    operations = [
        migrations.AddField(
            model_name='adherent',
            name='etudiant',
            field=models.CharField(blank=True, choices=[('0', 'Non'), ('1', 'Oui')], max_length=1, null=True),
        ),
    ]
