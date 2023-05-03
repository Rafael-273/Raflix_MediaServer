from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.generic import TemplateView


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


class Menu(TemplateView):
    template_name = 'parciais/menu.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context


class ConfigAll(ListView):
    model = models.Media
    template_name = 'front/config.html'
    context_object_name = 'movies'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CreateMovieView(View):
    def get(self, request):
        form = CreateMovieForm()
        return render(request, 'create/create_movie.html', {'form': form})

    def post(self, request):
        form = CreateMovieForm(request.POST, request.FILES)
        if form.is_valid():
            media = form.save(commit=False)
            media.save()
            movie = models.Movie.objects.create(
                media=media,
                description=form.cleaned_data['description'],
                short_description=form.cleaned_data['short_description'],
                duration=form.cleaned_data['duration'],
                classification=form.cleaned_data['classification']
            )
            return redirect('success')
        return render(request, 'create/create_movie.html', {'form': form})


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