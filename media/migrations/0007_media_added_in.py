# Generated by Django 4.1.3 on 2023-01-21 16:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0006_alter_movie_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='media',
            name='added_in',
            field=models.DateField(auto_now=True),
        ),
    ]
