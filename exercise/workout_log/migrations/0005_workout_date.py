# Generated by Django 2.2.6 on 2019-11-27 20:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout_log', '0004_auto_20191127_1150'),
    ]

    operations = [
        migrations.AddField(
            model_name='workout',
            name='date',
            field=models.DateField(default=datetime.date.today, help_text='date of workout'),
        ),
    ]