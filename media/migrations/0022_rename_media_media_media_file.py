# Generated by Django 4.1.3 on 2023-05-08 03:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0021_alter_user_photo'),
    ]

    operations = [
        migrations.RenameField(
            model_name='media',
            old_name='media',
            new_name='media_file',
        ),
    ]