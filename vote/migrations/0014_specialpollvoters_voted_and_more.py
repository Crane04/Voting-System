# Generated by Django 4.1 on 2023-08-13 03:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0013_alter_specialpollvoters_time_requested_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='specialpollvoters',
            name='voted',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='specialpollvoters',
            name='time_requested',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 13, 4, 52, 29, 788142)),
        ),
    ]
