# Generated by Django 3.2 on 2022-02-15 12:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_mfy'),
    ]

    operations = [
        migrations.AddField(
            model_name='mfy',
            name='rais_phone',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Telefon nomeri'),
        ),
    ]