# Generated by Django 3.2.3 on 2021-09-02 13:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inscription', '0023_auto_20210902_1418'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paiement',
            name='comment',
        ),
        migrations.AddField(
            model_name='historiquepaiement',
            name='comment',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Commentaire'),
        ),
    ]
