# Generated by Django 3.1.2 on 2021-01-06 03:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20201030_1105'),
    ]

    operations = [
        migrations.CreateModel(
            name='Web',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ph_num', models.CharField(max_length=10)),
                ('weights', models.BinaryField(null=True)),
            ],
        ),
    ]
