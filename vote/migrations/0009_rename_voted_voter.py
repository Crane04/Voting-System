# Generated by Django 4.1 on 2023-08-12 18:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vote', '0008_voted'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Voted',
            new_name='Voter',
        ),
    ]