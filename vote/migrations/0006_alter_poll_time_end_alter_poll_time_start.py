# Generated by Django 4.1 on 2023-08-07 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0005_poll_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='poll',
            name='time_end',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='poll',
            name='time_start',
            field=models.DateField(),
        ),
    ]
