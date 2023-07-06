# Generated by Django 3.2 on 2022-02-17 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_city_mfys_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='mfys_count',
            field=models.IntegerField(default=0, verbose_name='MFYlar soni'),
        ),
        migrations.AlterField(
            model_name='city',
            name='title',
            field=models.CharField(max_length=255, verbose_name='Shahar/tuman nomi'),
        ),
        migrations.AlterField(
            model_name='helperinfographic',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Rasm'),
        ),
        migrations.AlterField(
            model_name='leaderinfographic',
            name='image',
            field=models.ImageField(upload_to='', verbose_name='Rasm'),
        ),
    ]
