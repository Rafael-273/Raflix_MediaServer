from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView

class CustomLoginView(LoginView):
    template_name = 'front/login.html'
    authentication_form = LoginForm
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        print('remembado')
        remember_me = form.cleaned_data.get('remember_me')
        if remember_me:
            self.request.session.set_expiry(1209600) # 2 weeks
        else:
            self.request.session.set_expiry(0) # expire at browser close
        return super().form_valid(form)

    def get_success_url(self):
        if 'next' in self.request.GET:
            print('passou aqui??')
            next_url = self.request.GET['next']
        else:
            print('passou aqui')
            next_url = reverse_lazy('home')
        return next_url
    

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class Home(ListView):
    model = models.Media
    template_name = 'front/home.html'
    context_object_name = 'movies'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Movies(ListView):
    model = models.Media
    template_name = 'front/movies.html'
    context_object_name = 'movies'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Series(ListView):
    model = models.Media
    template_name = 'front/series.html'
    context_object_name = 'movies' 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Media(DetailView):
    model = models.Media
    template_name = 'front/movie.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Play(DetailView):
    model = models.Media
    template_name = 'front/play.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Trailer(DetailView):
    model = models.Media
    template_name = 'front/trailer.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class Favorites(ListView):
    model = models.Media
    template_name = 'front/favorites.html'
    context_object_name = 'movies' 
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

class User(ListView):
    model = models.User
    template_name = 'front/user.html'
    context_object_name = 'users'

class Config(ListView):
    model = models.Media
    template_name = 'front/config.html'
    context_object_name = 'users'

class Menu(TemplateView):
    template_name = 'parciais/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context

class ToggleFavorite(View):
    def post(self, request, *args, **kwargs):
        media_id = request.POST.get('media_id')
        media = models.Media.objects.get(id=media_id)
        media.favorited = not media.favorited
        media.save()
        return JsonResponse({'favorited': media.favorited})

class UpdateFavoriteView(View):
    def post(self, request, *args, **kwargs):
        movie_slug = request.POST.get('slug')
        movie = get_object_or_404(models.Media, slug=movie_slug)
        movie.favorited = not movie.favorited
        movie.save()
        return JsonResponse({'favorited': movie.favorited})

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            movies = models.Media.objects.filter(Q(title__icontains=query))
            print(movies)
            return render(request, 'front/search_results.html', {'movies': movies})
        else:
            return render(request, 'front/home.html')