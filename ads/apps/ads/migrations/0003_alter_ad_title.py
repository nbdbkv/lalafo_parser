# Generated by Django 3.2 on 2022-12-09 12:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ads', '0002_alter_ad_city'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ad',
            name='title',
            field=models.CharField(max_length=120, verbose_name='Заголовок'),
        ),
    ]
