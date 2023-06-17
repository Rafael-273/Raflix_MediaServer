# Generated by Django 4.1.3 on 2023-05-10 22:05

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0023_alter_user_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='telephone',
            field=models.CharField(blank=True, max_length=12, null=True, validators=[django.core.validators.RegexValidator(message="O número de telefone deve estar no formato: '+999999999'. Ele pode ter entre 9 e 11 dígitos.", regex='^\\+?1?\\d{9,11}$')]),
        ),
    ]