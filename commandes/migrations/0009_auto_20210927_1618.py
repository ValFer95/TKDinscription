# Generated by Django 3.2.3 on 2021-09-27 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0008_auto_20210927_1615'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandesdobok',
            name='statut_distribution',
        ),
        migrations.AlterField(
            model_name='commandesdobok',
            name='statut_commande',
            field=models.CharField(choices=[('1', 'En cours'), ('2', 'Commande distribuée'), ('3', 'Commande annulée')], default=1, max_length=1, verbose_name='Commande'),
        ),
    ]
