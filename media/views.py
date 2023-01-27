from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models

class Login(ListView):
    template_name = 'front/login.html'

class Home(ListView):
    model = models.Media
    template_name = 'front/home.html'
    context_object_name = 'movies'

class Movies(ListView):
    model = models.Media
    template_name = 'front/movies.html'
    context_object_name = 'movies'

class Series(ListView):
    model = models.Media
    template_name = 'front/series.html'
    context_object_name = 'movies' 

class Media(ListView):
    model = models.Media
    template_name = 'front/movie.html'
    context_object_name = 'movies'

class User(ListView):
    pass 

class Favorites(ListView):
    pass 