from django.contrib import admin
from . import models

admin.site.register(models.Admin)
admin.site.register(models.User)
admin.site.register(models.Evaluation)
admin.site.register(models.Media)
admin.site.register(models.Movie)
admin.site.register(models.Serie)
admin.site.register(models.Season)
admin.site.register(models.Episode)
admin.site.register(models.Genre)
admin.site.register(models.Movie_has_genre)
admin.site.register(models.Serie_has_genre)