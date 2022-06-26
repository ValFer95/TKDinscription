# Generated by Django 3.2.3 on 2022-06-26 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inscription', '0026_alter_adherent_taille'),
        ('cotisation', '0017_maintenance'),
    ]

    operations = [
        migrations.CreateModel(
            name='MailingRelance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nature_relance', models.CharField(max_length=20, verbose_name='Nature mail relance')),
                ('date_crea', models.DateTimeField(auto_now_add=True)),
                ('date_last_modif', models.DateTimeField(auto_now=True)),
                ('famille', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.famille')),
                ('saison', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cotisation.saison')),
            ],
        ),
    ]
