# Generated by Django 4.1.3 on 2023-05-02 01:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0019_remove_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='password',
            field=models.CharField(max_length=8),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=50),
        ),
    ]
