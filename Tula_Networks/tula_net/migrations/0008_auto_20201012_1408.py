# Generated by Django 3.1.1 on 2020-10-12 11:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tula_net', '0007_auto_20201012_1407'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeder',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='feeders', to='tula_net.section', verbose_name='СкШ'),
        ),
    ]
