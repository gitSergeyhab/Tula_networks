# Generated by Django 3.1.1 on 2020-11-01 10:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tula_net', '0003_auto_20201031_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='feeder',
            name='reliability_category',
        ),
    ]
