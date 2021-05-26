# Generated by Django 3.2.3 on 2021-05-26 14:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0003_auto_20210526_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='adhfamille',
            name='adherent',
        ),
        migrations.RemoveField(
            model_name='adhfamille',
            name='famille',
        ),
        migrations.AddField(
            model_name='adherent',
            name='contact',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inscription.contact'),
        ),
        migrations.AddField(
            model_name='adherent',
            name='famille',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='inscription.famille'),
        ),
        migrations.AlterField(
            model_name='adherent',
            name='ddn',
            field=models.DateField(verbose_name='Date de naissance'),
        ),
        migrations.AlterField(
            model_name='adherent',
            name='email_adh',
            field=models.EmailField(blank=True, max_length=200, null=True, verbose_name='E-mail adhérent'),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email_adh',
            field=models.EmailField(max_length=200, verbose_name='E-mail contact'),
        ),
        migrations.AlterField(
            model_name='famille',
            name='nom_famille',
            field=models.CharField(max_length=80, verbose_name='Nom de la famille'),
        ),
        migrations.DeleteModel(
            name='AdhContact',
        ),
        migrations.DeleteModel(
            name='AdhFamille',
        ),
    ]
