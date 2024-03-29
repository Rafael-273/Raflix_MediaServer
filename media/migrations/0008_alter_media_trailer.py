# Generated by Django 4.1.3 on 2023-01-21 17:15

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0007_media_added_in'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='trailer',
            field=models.FileField(upload_to='static/media/trailer', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv'])]),
        ),
    ]
