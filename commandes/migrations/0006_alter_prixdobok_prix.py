# Generated by Django 3.2.3 on 2021-09-27 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0005_alter_prixdobok_prix'),
    ]

    operations = [
        migrations.AlterField(
            model_name='prixdobok',
            name='prix',
            field=models.CharField(max_length=12, verbose_name='Prix'),
        ),
    ]
