# Generated by Django 3.2 on 2022-12-09 05:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='city',
            field=models.CharField(max_length=60, verbose_name='Город'),
        ),
    ]
