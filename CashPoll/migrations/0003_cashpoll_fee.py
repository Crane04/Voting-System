# Generated by Django 4.1 on 2023-08-15 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CashPoll', '0002_delete_cashpollvoter'),
    ]

    operations = [
        migrations.AddField(
            model_name='cashpoll',
            name='fee',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
