# Generated by Django 3.1.2 on 2021-01-06 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_auto_20210106_0402'),
    ]

    operations = [
        migrations.AddField(
            model_name='web',
            name='name',
            field=models.CharField(default='', max_length=30),
        ),
    ]
