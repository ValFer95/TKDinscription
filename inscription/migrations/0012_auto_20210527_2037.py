# Generated by Django 3.2.3 on 2021-05-27 18:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0011_alter_adherent_etudiant'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adherent',
            name='contact',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.contact'),
        ),
        migrations.AlterField(
            model_name='adherent',
            name='famille',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.famille'),
        ),
    ]