# Generated by Django 4.1 on 2023-08-13 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vote', '0010_specialpoll'),
    ]

    operations = [
        migrations.AlterField(
            model_name='specialpoll',
            name='voters',
            field=models.PositiveIntegerField(default=0),
        ),
    ]