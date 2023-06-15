from django.urls import path, include, re_path
from django.views.generic.base import RedirectView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/favicon.ico')),#correção bug favicon
    path('', views.Home.as_view(), name='home'),
    path('', include(tf_urls)),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('movies', views.Movies.as_view(), name='movies'),
    path('series', views.Series.as_view(), name='series'),
    path('user', views.User.as_view(), name='user'),
    path('favorites', views.Favorites.as_view(), name='favorites'),
    path('play/<slug>', views.Play.as_view(), name='play'),
    path('trailer/<slug>', views.Trailer.as_view(), name='trailer'),
    path('toggle_favorite/', views.ToggleFavorite.as_view(), name='toggle_favorite'),
    path('update_favorite/', views.UpdateFavoriteView.as_view(), name='update_favorite'),
    path('search/', views.SearchView.as_view(), name='search'),
    path('config', views.ConfigAll.as_view(), name='config'),
    path('create_movie', views.CreateMovieView.as_view(), name='create_movie'),
    path('create_user', views.CreateUserView.as_view(), name='create_user'),
    path('edit_movie/<slug>', views.EditMovieView.as_view(), name='edit_movie'),
    path('list_movies', views.ListMoviesView.as_view(), name='list_movies'),
    path('edit_user/<int:id>', views.EditUserView.as_view(), name='edit_user'),
    path('<slug>', views.Media.as_view(), name='media'),
]

# Adicione esta linha se você quiser servir arquivos estáticos durante o desenvolvimento
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
