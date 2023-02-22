from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('login', views.Login.as_view(), name='login'),
    path('movies', views.Movies.as_view(), name='movies'),
    path('series', views.Series.as_view(), name='series'),
    path('favorites', views.Favorites.as_view(), name='favorites'),
    path('play/<slug>', views.Play.as_view(), name='play'),
    path('trailer/<slug>', views.Trailer.as_view(), name='trailer'),
    path('user', views.User.as_view(), name='user'),
    path('toggle_favorite/', views.ToggleFavorite.as_view(), name='toggle_favorite'),
    path('update_favorite/', views.UpdateFavoriteView.as_view(), name='update_favorite'),
    path('<slug>', views.Media.as_view(), name='media'),
]

