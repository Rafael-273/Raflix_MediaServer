# Generated by Django 4.1.3 on 2023-05-10 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0024_alter_user_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
