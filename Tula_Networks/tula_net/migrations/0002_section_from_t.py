# Generated by Django 3.1.1 on 2020-10-12 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tula_net', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='section',
            name='from_T',
            field=models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='питается от Т №'),
        ),
    ]
