# Generated by Django 4.1.3 on 2023-07-06 05:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0029_remove_media_title_img'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='short_description',
        ),
    ]