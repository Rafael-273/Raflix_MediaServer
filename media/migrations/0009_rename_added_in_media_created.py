# Generated by Django 4.1.4 on 2023-01-24 04:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0008_alter_media_trailer'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='added_in',
            new_name='created',
        ),
    ]
