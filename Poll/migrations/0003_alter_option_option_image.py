# Generated by Django 4.1 on 2023-08-17 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Poll', '0002_option_option_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='option_image',
            field=models.ImageField(default='', upload_to='poll/option'),
        ),
    ]
