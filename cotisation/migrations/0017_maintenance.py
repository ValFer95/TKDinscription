# Generated by Django 3.2.3 on 2022-06-26 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0016_remove_saison_saison_prochaine'),
    ]

    operations = [
        migrations.CreateModel(
            name='Maintenance',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('maintenance', models.BooleanField(default=False)),
            ],
        ),
    ]