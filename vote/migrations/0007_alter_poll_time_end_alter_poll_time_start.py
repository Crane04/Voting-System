# Generated by Django 4.1 on 2023-08-07 21:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0006_alter_poll_time_end_alter_poll_time_start'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='time_end',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='poll',
            name='time_start',
            field=models.DateTimeField(),
        ),
    ]
