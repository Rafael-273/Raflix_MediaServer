from django.db import models
from embed_video.fields import EmbedVideoField
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator

class Admin(models.Model):
    admin = models.CharField(
        default='Y',
        max_length=1,
        choices=(
            ('Y', 'Admin'),
            ('N', "Not Admin ")
        )
        )

    def __str__(self):
        return self.admin
        
    class Meta:
        verbose_name = 'Admin'
        verbose_name_plural = 'Admin'

class User(models.Model):
    name = models.CharField(max_length=55, blank=False)
    photo = models.ImageField(upload_to='static/media/img', default='img' ,blank=True, null=True)
    email = models.EmailField(blank=False)
    password = models.CharField(max_length=20, blank=False, null=False)
    telephone = models.IntegerField(blank=True)
    admin = models.ForeignKey(
        'Admin', related_name='user_has_admin' ,on_delete=models.CASCADE)

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        origin_width, origin_height = img_pil.size

        if origin_width <= new_width:
            img_pil.close()
            return

        new_height = round((new_width * origin_height) / origin_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.photo:
            self.resize_image(self.photo, max_image_size)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

class Evaluation(models.Model):
    evaluation = models.CharField(
        default='Y',
        max_length=1,
        choices=(
            ('Y', 'Like'),
            ('N', "Don't Like")
        )
        )
    user = models.ForeignKey(
        'User', related_name='evaluation_has_user', on_delete=models.CASCADE)
    media = models.ForeignKey(
        'Media', related_name='media_has_user', on_delete=models.CASCADE)
    
class Media(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    release_year = models.IntegerField(blank=True)
    poster = models.ImageField(blank=True)
    media = models.FileField(
        null=False,
        blank=False,
        upload_to='static/media/video',
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv'])
        ])
    trailer = EmbedVideoField()

    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        origin_width, origin_height = img_pil.size

        if origin_width <= new_width:
            print('largura igual ou menor que a original')
            img_pil.close()
            return

        new_height = round((new_width * origin_height) / origin_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)
        new_img.save(
            img_full_path,
            optimize=True,
            quality=50
        )

        print('imagem redimensionada')

    def save(self, *args, **kwargs):
        if not self.slug:
            slug = f'{slugify(self.title)}'
            self.slug = slug

        super().save(*args, **kwargs)

        max_image_size = 800

        if self.poster:
            self.resize_image(self.poster, max_image_size)

    def __str__(self):
        return self.title

class Movie(models.Model):
    description = models.TextField()
    duration = models.FloatField(blank=True)
    media = models.ForeignKey(
        'Media', related_name='media_has_movie', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

class Serie(models.Model):
    description = models.TextField()
    class Meta:
        verbose_name = 'Serie'
        verbose_name_plural = 'Series'

class Season(models.Model):
    number = models.IntegerField()
    serie = models.ForeignKey(
        'Serie', related_name='serie_has_season', on_delete=models.CASCADE)

    def __str__(self):
        return f'Season {self.number}'

    class Meta:
        verbose_name = 'Season'
        verbose_name_plural = 'Seasons'

class Episode(models.Model):
    number = models.IntegerField()
    description = models.TextField()
    duration = models.FloatField(blank=True)
    season = models.ForeignKey(
        'Season', related_name='season_has_episode', on_delete=models.CASCADE)
    media = models.ForeignKey(
        'Media', related_name='media_has_episode', on_delete=models.CASCADE)

    def __str__(self):
        return f'Episode {self.number}'

    class Meta:
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'


class Genre(models.Model):
    category = models.CharField(
        default='N',
        max_length=2,
        choices=(
            ('N', 'Não Definido'),
            ('A', 'Ação'),
            ('AN', 'Animação'),
            ('AV', 'Aventura'),
            ('C', 'Comédia'),
            ('CR', 'Comédia Romântica'),
            ('D', 'Documentário'),
            ('F', 'Ficção Científica'),
            ('G', 'Guerra'),
            ('M', 'Musical'),
            ('R', 'Romance'),
            ('T', 'Terror')
        )
        )

    def __str__(self):
        return self.category 

    class Meta:
        verbose_name = 'Genre'
        verbose_name_plural = 'Genres'

class Movie_has_genre(models.Model):
    genre = models.ForeignKey(
        'Genre', related_name='genre_has_movie', on_delete=models.CASCADE)
    movie = models.ForeignKey(
        'Movie', related_name='movie_has_genre', on_delete=models.CASCADE)

class Serie_has_genre(models.Model):
    genre = models.ForeignKey(
        'Genre', related_name='genre_has_serie', on_delete=models.CASCADE)
    serie = models.ForeignKey(
        'Serie', related_name='serie_has_genre', on_delete=models.CASCADE)