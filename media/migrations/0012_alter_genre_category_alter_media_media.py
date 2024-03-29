# Generated by Django 4.1.3 on 2023-02-16 15:58

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('media', '0011_alter_genre_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genre',
            name='category',
            field=models.CharField(choices=[('N', 'Não Definido'), ('A', 'Ação'), ('AN', 'Animação'), ('AV', 'Aventura'), ('C', 'Comédia'), ('CR', 'Comédia Romântica'), ('D', 'Documentário'), ('F', 'Ficção Científica'), ('G', 'Guerra'), ('M', 'Musical'), ('R', 'Romance'), ('T', 'Terror'), ('MA', 'Marvel'), ('LA', 'Lançamento')], default='N', max_length=2),
        ),
        migrations.AlterField(
            model_name='media',
            name='media',
            field=models.FileField(upload_to='static/media/video', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['MOV', 'avi', 'mp4', 'webm', 'mkv', 'h264'])]),
        ),
    ]
