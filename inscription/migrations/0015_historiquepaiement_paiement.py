# Generated by Django 3.2.3 on 2021-05-29 12:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0012_categorie_etudiant'),
        ('inscription', '0014_alter_adherent_saison_certif_med'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_cotis', models.IntegerField(default=0, verbose_name='Montant cotisation')),
                ('paye', models.CharField(choices=[('0', 'Non'), ('1', 'Partiellement'), ('2', 'Oui')], default=0, max_length=1, verbose_name='Cotisation réglée')),
                ('comment', models.CharField(blank=True, max_length=255, null=True, verbose_name='Commentaire')),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.famille')),
                ('saison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotisation.saison')),
            ],
        ),
        migrations.CreateModel(
            name='HistoriquePaiement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('montant_regle', models.IntegerField(default=0, verbose_name='Montant réglé')),
                ('type_rglmt', models.CharField(blank=True, choices=[('0', 'Non'), ('1', 'Partiellement'), ('2', 'Oui')], max_length=1, null=True, verbose_name='Type règlement')),
                ('date_rglt', models.DateTimeField(blank=True, null=True, verbose_name='Date règlement')),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.famille')),
                ('saison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotisation.saison')),
            ],
        ),
    ]
