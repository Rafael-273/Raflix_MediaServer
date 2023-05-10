from django.db import models
from embed_video.fields import EmbedVideoField
from PIL import Image
import os
from django.conf import settings
from django.utils.text import slugify
from django.core.validators import FileExtensionValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractUser, Group, Permission

class User(AbstractUser):
    photo = models.ImageField(upload_to='static/media/user', blank=True, null=True)
    telephone = models.IntegerField(blank=False, null=True)
    groups = models.ManyToManyField(Group, related_name='user_group_set', null=True)

    def __str__(self):
        return self.username

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
        self.set_password(self.password)
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.photo:
            self.resize_image(self.photo, max_image_size)

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'auth_user'

class Media(models.Model):
    title = models.CharField(max_length=255, blank=False)
    slug = models.SlugField(unique=True, blank=True, null=True)
    release_year = models.IntegerField(blank=True)
    favorited = models.BooleanField(default=False)
    poster = models.ImageField(upload_to='static/media/poster', blank=True)
    banner = models.ImageField(upload_to='static/media/banner', blank=True, null=True)
    title_img = models.ImageField(upload_to='static/media/title', blank=True)
    media_file = models.FileField(
        null=False,
        blank=False,
        upload_to='static/media/video',
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','h264'])
        ])
    trailer = models.FileField(
        null=False,
        blank=False,
        upload_to='static/media/trailer',
        validators=[
            FileExtensionValidator(allowed_extensions=['MOV','avi','mp4','webm','mkv','h264'])
        ])
    created = models.DateField(auto_now = True)

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

    def getClassification(self):
        movies = self.media_has_movie.all()
        for movie in movies:
            return movie.classification

    def getDuration(self):
        movies = self.media_has_movie.all()
        for movie in movies:
            return movie.duration
    
    def getDescription(self):
        movies = self.media_has_movie.all()
        for movie in movies:
            return movie.description

    def getShortDescription(self):
        movies = self.media_has_movie.all()
        for movie in movies:
            return movie.short_description

    def getCategory(self):
        movies = self.media_has_movie.all()
        for movie in movies:
            genres = [related.genre.get_genre() for related in movie.movie_has_genre.all()]
            return genres

class Movie(models.Model):
    description = models.TextField()
    short_description = models.TextField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=10)
    classification = models.IntegerField(default=12)
    media = models.ForeignKey(
        'Media', related_name='media_has_movie', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Movie'
        verbose_name_plural = 'Movies'

    def __str__(self):
        return '{0}'.format(self.media)

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

genre_choices = (('N', 'Não Definido'),
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
            ('T', 'Terror'),
            ('MA', 'Marvel'),
            ('LA', 'Lançamento'))

class Genre(models.Model):
    category = models.CharField(
        default='N',
        max_length=2,
        choices=genre_choices
        )

    def get_genre(self):
        for genre_content in genre_choices:
            if self.category in genre_content:
                return genre_content[1]

    def __str__(self):
        return self.get_genre() 

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