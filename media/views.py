from django.shortcuts import render
from django.views.generic.list import ListView
from django.views import View
from . import models


class Home(ListView):
    model = models.Media
    template_name = 'front/home.html'
    context_object_name = 'movies'

class Movies(ListView):
    model = models.Media
    template_name = 'front/movie.html'
    context_object_name = 'movies'

class Series(ListView):
    pass  

class Media(ListView):
    pass 

class User(ListView):
    pass 

class Favorites(ListView):
    pass 