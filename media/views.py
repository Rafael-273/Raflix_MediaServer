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
# from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from .forms import CreateMovieForm, CustomAuthenticationForm, EditMovieForm, EditUserForm, SmartCreateMovieForm
from django_otp import login as otp_login
from .forms import CreateUserForm
from django.contrib.auth import login
from utils.utils import process_movie
from django.contrib import messages
import os
from django.conf import settings
import shutil


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()  # Obtém a instância do objeto Media
        video_path = movie.media_file.url  # Obtém o caminho do vídeo
        context['video_path'] = video_path  # Adiciona a variável de contexto
        return context


class Trailer(DetailView):
    model = models.Media
    template_name = 'front/trailer.html'
    context_object_name = 'movie'
    slug_url_kwarg = 'slug'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        movie = self.get_object()
        video_path = movie.trailer.url
        context['video_path'] = video_path
        return context


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


class SmartCreateMovieView(View):
    model = models.Media
    template_name = 'create/smart_create_movie.html'
    form_class = SmartCreateMovieForm

    def get(self, request):
        form = self.form_class
        return render(request, 'create/smart_create_movie.html', {'form': form})

    def post(self, request):
        page_source = request.POST.get('page_source')
        if page_source == 'pagina1':
            movie_title = request.POST.get('movie_title')

            if movie_title:
                print(movie_title)

                success = process_movie(movie_title)

                if success == "not_found":
                    messages.error(request, f"Ops! Parece que '{movie_title}' não foi encontrado (•ิ_•ิ)")
                    self.delete_related_files(movie_title)
                elif success == "error_process":
                    messages.error(request, f"O processamento de '{movie_title}' foi um verdadeiro drama tecnológico, com twists inesperados. Tente Novamente (•ิ_•ิ)")
                    self.delete_related_files(movie_title)
                elif success == "existing_movie":
                    messages.error(request, "Opa guerreiro! Nós já temos esse filme na lista (/•ิ_•ิ)/")
                elif success:
                    messages.success(request, f"Prepare a pipoca! '{movie_title}' foi encontrado e o download foi iniciado ◕‿◕")
                    self.delete_non_mkv_files()
                else:
                    messages.error(request, f"Um bug estranho roubou a cena enquanto processávamos '{movie_title}'. Parece que os bytes estão atuando por conta própria ⊙▂⊙")
                    self.delete_related_files(movie_title)

            return redirect(reverse_lazy('home'))

        elif page_source == 'pagina2':
            form = self.form_class(request.POST)
            if form.is_valid():
                title = form.cleaned_data['title']
                print(title)

                success = process_movie(title)

                if success == "not_found":
                    messages.error(request, f"Ops! Parece que '{title}' não foi encontrado (•ิ_•ิ)")
                    self.delete_related_files(title)
                elif success == "error_process":
                    messages.error(request, f"O processamento de '{title}' foi um verdadeiro drama tecnológico, com twists inesperados. Tente Novamente (•ิ_•ิ)")
                    self.delete_related_files(title)
                elif success == "existing_movie":
                    messages.error(request, "Opa guerreiro! Nós já temos esse filme na lista (/•ิ_•ิ)/")
                elif success:
                    messages.success(request, f"Prepare a pipoca! '{title}' foi encontrado e o download foi iniciado ◕‿◕")
                    self.delete_non_mkv_files()
                else:
                    messages.error(request, f"Um bug estranho roubou a cena enquanto processávamos '{title}'. Parece que os bytes estão atuando por conta própria ⊙▂⊙")
                    self.delete_related_files(title)

                return redirect(reverse_lazy('smart_create_movie'))

            else:
                form = self.form_class()
            return render(request, self.template_name, {'form': form})

    def delete_related_files(self, title):
        clean_title = title.replace(':', '').replace(' ', '_').replace('.', '_')
        trailer_path = os.path.join(settings.BASE_DIR, f'img/static/media/trailer/{clean_title}_trailer.mp4')
        movie_path = os.path.join(settings.BASE_DIR, f'img/static/media/video/{clean_title}_movie.mkv')
        poster_path = os.path.join(settings.BASE_DIR, f'img/static/media/poster/{clean_title}_poster.jpg')

        if os.path.exists(trailer_path):
            os.remove(trailer_path)
        if os.path.exists(movie_path):
            os.remove(movie_path)
        if os.path.exists(poster_path):
            os.remove(poster_path)

    def delete_non_mkv_files(self):
        video_folder = os.path.join(settings.BASE_DIR, 'img/static/media/video')

        for item_name in os.listdir(video_folder):
            item_path = os.path.join(video_folder, item_name)

            if os.path.isfile(item_path) and not item_name.endswith('.mkv'):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                # Remova o diretório e todo o seu conteúdo (recursivamente)
                shutil.rmtree(item_path)


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
            )
            media.save()

            genre = models.Genre(
                category = form.cleaned_data['category']
            )
            genre.save()

            movie = models.Movie(
                description=form.cleaned_data['description'],
                duration=form.cleaned_data['duration'],
                classification=form.cleaned_data['classification'],
                media=media,
            )
            movie.save()

            movie_has_genre = models.Movie_has_genre(
                genre=genre,
                movie=movie
            )
            movie_has_genre.save()

            return redirect(reverse_lazy('home'))

        else:
            print(form.errors)
            # Se o formulário não for válido, exiba os erros
            return render(request, 'create/create_movie.html', {'form': form, 'errors': form.errors})


class ListMoviesView(View):
    def get(self, request):
        movies = models.Media.objects.all()
        return render(request, 'edit/list_movies.html', {'movies': movies})


class ListUsersView(View):
    def get(self, request):
        users = models.User.objects.all()
        return render(request, 'edit/list_users.html', {'users': users})


class ListMoviesDeleteView(View):
    def get(self, request):
        movies = models.Media.objects.all()
        return render(request, 'remove/list_movies_delete.html', {'movies': movies})


class ListUsersDeleteView(View):
    def get(self, request):
        users = models.User.objects.all()
        return render(request, 'remove/list_users_delete.html', {'users': users})


class EditMovieView(View):
    def get(self, request, slug):
        media = models.Media.objects.get(slug=slug)
        movie = media.media_has_movie.first()
        form = EditMovieForm(instance=movie)
        return render(request, 'edit/edit_movie.html', {'form': form, 'movie': movie})

    def post(self, request, slug):
        media = get_object_or_404(models.Media, slug=slug)
        movie = media.media_has_movie.first()
        form = EditMovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            if movie:
                movie = form.save()

                genre = models.Genre(
                    category = form.cleaned_data['category']
                )
                genre.save()

                movie_has_genre = models.Movie_has_genre(
                    genre=genre,
                    movie=movie
                )
                movie_has_genre.save()

                return redirect(reverse_lazy('home'))
        return render(request, 'edit/edit_movie.html', {'form': form, 'movie': movie})

class CreateUserView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'create/create_user.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('home')
        return render(request, 'create/create_user.html', {'form': form})


class EditUserView(View):
    def get(self, request, id):
        user = models.User.objects.get(id=id)
        form = EditUserForm(instance=user)
        return render(request, 'edit/edit_user.html', {'form': form, 'user': user})
    def post(self, request, id):
        user = get_object_or_404(models.User, id=id)
        form = EditUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            if user:
                user = form.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect(reverse_lazy('home'))
        return render(request, 'edit/edit_user.html', {'form': form, 'user': user})


class DeleteMovieView(View):
    def get(self, request, slug):
        movie = get_object_or_404(models.Media, slug=slug)
        return render(request, 'remove/remove_movies.html', {'movie': movie})

    def post(self, request, slug):
        movie = get_object_or_404(models.Media, slug=slug)
        self.delete_related_files(movie.title)
        self.delete_non_mkv_files()
        movie.delete()
        return redirect('home')

    def delete_related_files(self, title):
        clean_title = title.replace(':', '').replace(' ', '_').replace('.', '_')
        trailer_path = os.path.join(settings.BASE_DIR, f'img/static/media/trailer/{clean_title}_trailer.mp4')
        movie_path = os.path.join(settings.BASE_DIR, f'img/static/media/video/{clean_title}_movie.mkv')
        poster_path = os.path.join(settings.BASE_DIR, f'img/static/media/poster/{clean_title}_poster.jpg')

        if os.path.exists(trailer_path):
            os.remove(trailer_path)
        if os.path.exists(movie_path):
            os.remove(movie_path)
        if os.path.exists(poster_path):
            os.remove(poster_path)

    def delete_non_mkv_files(self):
        video_folder = os.path.join(settings.BASE_DIR, 'img/static/media/video')

        for item_name in os.listdir(video_folder):
            item_path = os.path.join(video_folder, item_name)

            if os.path.isfile(item_path) and not item_name.endswith('.mkv'):
                os.remove(item_path)
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)


class DeleteUserView(View):
    def get(self, request, id):
        user = get_object_or_404(models.User, id=id)
        return render(request, 'remove/remove_users.html', {'user': user})

    def post(self, request, id):
        user = get_object_or_404(models.User, id=id)
        user.delete()
        return redirect('home')


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