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
# from .forms import LoginForm
from django.contrib.auth import authenticate, login
from django.views.generic import TemplateView
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.fields import BooleanField
from django.db.models import Q, Case, When, BooleanField, Exists, Subquery, OuterRef
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django import forms
from .forms import CreateMovieForm
from django.views.generic.edit import CreateView
from django.views.generic import FormView

class CustomLoginView(FormView):
    template_name = 'front/login.html'
    success_url = reverse_lazy('home')
    
    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        remember_me = request.POST.get('remember_me')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            
            if remember_me:
                request.session.set_expiry(1209600) # 2 weeks
            else:
                request.session.set_expiry(0) # expire at browser close
            
            return HttpResponseRedirect(self.get_success_url())
        else:
            return self.form_invalid(None)
    
    def get_success_url(self):
        if 'next' in self.request.GET:
            next_url = self.request.GET['next']
        else:
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


    def get_queryset(self):
        user_id = self.request.user.id
        
        # Subquery para obter os favoritos do usuário
        favorites_subquery = models.Favorite.objects.filter(
            user_id=user_id,
            media_id=OuterRef('pk'),
        ).values('favorited')[:1]
        
        # Annotation para adicionar a coluna `favorited`
        queryset = self.model.objects.annotate(
            favorited=Subquery(favorites_subquery),
        )
        
        return queryset
    
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     user_id = self.request.user.id
    #     user = get_object_or_404(models.User, id=user_id)
    #     media = context['movie']
    #     favorite = models.Favorite.objects.filter(user=user, media=media, favorited=True).first()
    #     context['favorited'] = favorite is not None
    #     return context

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

# @method_decorator(csrf_exempt, name='dispatch')
# class Favorites(ListView):
#     model = models.Media
#     template_name = 'front/favorites.html'
#     context_object_name = 'movies'

#     def get_queryset(self):
#         if self.request.user.is_authenticated:
#             user_id = self.request.user.id
#             user = get_object_or_404(models.User, id=user_id)
#             favorites = models.Favorite.objects.filter(user=user)
#             self.favorite_slugs = [favorite.media.slug for favorite in favorites]   
#             queryset = models.Media.objects.filter(slug__in=self.favorite_slugs, media_has_user__favorited=True)
#             return queryset
#         else:
#             return models.Media.objects.none()

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         favorite_movies = models.Media.objects.filter(slug__in=self.favorite_slugs, media_has_user__favorited=True)
#         context['favorite_movies'] = favorite_movies
#         return context

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

# class User(ListView):
#     model = models.User
#     template_name = 'front/user.html'
#     context_object_name = 'users'

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

class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q')
        if query:
            movies = models.Media.objects.filter(Q(title__icontains=query))
            print(movies)
            return render(request, 'front/search_results.html', {'movies': movies})
        else:
            return render(request, 'front/home.html')
            

# @method_decorator(csrf_exempt, name='dispatch')
# class FavoriteMovieView(View):
#     def post(self, request):
#         if request.method == "POST":
#             user_id = request.user.id
#             slug = request.POST.get("slug")
#             is_favorited = request.POST.get("is_favorited")
#             movie = get_object_or_404(models.Media, slug=slug)
#             user = get_object_or_404(models.User, id=user_id)
#             favorite, created = models.Favorite.objects.get_or_create(user=user, media=movie)
#             if not created:
#                 favorite.favorited = not favorite.favorited
#                 favorite.save()
#                 return JsonResponse({"success": True, "favorited": favorite.favorited})
#             else:
#                 favorite.favorited = True
#                 favorite.save()
#                 return JsonResponse({"success": False, "favorited": True})
            
    
#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super().dispatch(*args, **kwargs)

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
