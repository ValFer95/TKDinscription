# Generated by Django 3.2.3 on 2021-09-27 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('commandes', '0007_auto_20210927_1352'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='commandesdobok',
            name='voeu_commande',
        ),
        migrations.AddField(
            model_name='commandesdobok',
            name='statut_commande',
            field=models.CharField(choices=[('1', 'En cours'), ('2', 'Commande livrée'), ('3', 'Commande annulée')], default=1, max_length=1, verbose_name='Commande'),
        ),
        migrations.AlterField(
            model_name='commandesdobok',
            name='tarif_info',
            field=models.CharField(max_length=12, verbose_name='Tarif informatif (€)'),
        ),
    ]