# Generated by Django 4.1.3 on 2023-05-03 00:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0020_alter_user_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='static/media/user'),
        ),
    ]
