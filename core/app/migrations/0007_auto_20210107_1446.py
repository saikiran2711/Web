# Generated by Django 3.1.2 on 2021-01-07 14:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_auto_20210107_1435'),
    ]

    operations = [
        migrations.AlterField(
            model_name='web',
            name='weights',
            field=models.CharField(default='', max_length=20000),
        ),
    ]
