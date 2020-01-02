# Generated by Django 2.2.6 on 2019-11-27 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_log', '0003_auto_20191127_1139'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='distance',
            field=models.DecimalField(decimal_places=2, help_text='enter distance in miles (up to 2 decimal places)', max_digits=5),
        ),
        migrations.AlterField(
            model_name='workout',
            name='duration',
            field=models.DurationField(help_text='hh:mm:ss'),
        ),
    ]
