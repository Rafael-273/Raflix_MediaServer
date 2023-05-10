from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from . import models
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .forms import LoginForm
# from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from .forms import CreateMovieForm, CustomAuthenticationForm
from django_otp import login as otp_login
from .forms import CreateUserForm
from django.contrib.auth import login

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')
    

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'two_factor/core/login.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        """
        Security check complete. Log the user in.
        """
        # Ensure the user-originating redirection url is safe.
        self.check_and_update_redirect_url()
        # Redirect to the success URL.
        return otp_login(self.request, form.get_user())
    

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

            media = models.Media(
                media_file = form.cleaned_data['media_file'],
                trailer = form.cleaned_data['trailer'], 
                title = form.cleaned_data['title'],
                release_year = form.cleaned_data['release_year'],
                poster = form.cleaned_data['poster'],
                banner = form.cleaned_data['banner'],
                title_img = form.cleaned_data['title_img'],
            )
            media.save()

            movie = models.Movie(
                description=form.cleaned_data['description'],
                short_description=form.cleaned_data['short_description'],
                duration=form.cleaned_data['duration'],
                classification=form.cleaned_data['classification'],
                media=media,
            )
            movie.save()

            return redirect(reverse_lazy('home'))
        return render(request, 'create/create_movie.html', {'form': form})


class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'create/create_user.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.telephone = form.cleaned_data.get('telephone')
            user.photo = form.cleaned_data.get('photo')
            user.save()
            login(request, user)
            return redirect('home')
        return render(request, 'create/create_user.html', {'form': form})


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