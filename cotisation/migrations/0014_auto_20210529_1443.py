# Generated by Django 3.2.3 on 2021-05-29 12:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cotisation', '0013_auto_20210529_1440'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorie',
            name='code_catg',
            field=models.CharField(max_length=6, verbose_name='Code catégorie'),
        ),
        migrations.AlterField(
            model_name='discipline',
            name='code_discipl',
            field=models.CharField(max_length=10, verbose_name='Code discipline'),
        ),
    ]