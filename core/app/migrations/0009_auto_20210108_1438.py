# Generated by Django 3.1.2 on 2021-01-08 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20210108_0816'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='web',
            name='id',
        ),
        migrations.AlterField(
            model_name='web',
            name='ph_num',
            field=models.CharField(max_length=10, primary_key=True, serialize=False),
        ),
    ]
