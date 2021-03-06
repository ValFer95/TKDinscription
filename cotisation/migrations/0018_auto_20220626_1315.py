# Generated by Django 3.2.3 on 2022-06-26 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0017_maintenance'),
    ]

    operations = [
        migrations.AddField(
            model_name='maintenance',
            name='maintenance_en_cours',
            field=models.BooleanField(default=False, verbose_name='Maintenance en cours'),
        ),
        migrations.AlterField(
            model_name='maintenance',
            name='maintenance',
            field=models.CharField(max_length=12, verbose_name='Maintenance'),
        ),
    ]
