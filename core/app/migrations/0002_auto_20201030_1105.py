# Generated by Django 3.1.2 on 2020-10-30 11:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pic',
            name='ph_num',
            field=models.CharField(max_length=10),
        ),
    ]
