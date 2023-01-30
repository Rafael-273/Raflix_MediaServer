from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models

class Login(ListView):
    model = models.Media
    template_name = 'front/login.html'
    context_object_name = 'movies'

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

class Media(DetailView):
    model = models.Media
    template_name = 'front/movie.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'

class User(ListView):
    pass 

class Favorites(ListView):
    pass 