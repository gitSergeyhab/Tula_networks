# Generated by Django 3.1.1 on 2020-10-12 10:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tula_net', '0003_auto_20201012_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feeder',
            name='attention',
            field=models.BooleanField(default=False, verbose_name='!!!'),
        ),
        migrations.AlterField(
            model_name='feeder',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feeders', to='tula_net.section', verbose_name='СкШ'),
        ),
    ]
