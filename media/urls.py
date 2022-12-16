from django.urls import path
from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('/movies', views.Movies.as_view(), name='movies'),
    path('/series', views.Series.as_view(), name='series'),
    path('<slug>', views.Media.as_view(), name='media'),
    path('/user', views.User.as_view(), name='user'),
    path('/favorites', views.Favorites.as_view(), name='favorites'),
]