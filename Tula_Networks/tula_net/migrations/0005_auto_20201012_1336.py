# Generated by Django 3.1.1 on 2020-10-12 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tula_net', '0004_auto_20201012_1328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeder',
            name='res',
            field=models.CharField(blank=True, max_length=32, null=True, verbose_name='РЭС'),
        ),
    ]
