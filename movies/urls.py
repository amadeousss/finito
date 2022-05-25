from django.urls import path
from .views import MovieList, movie_search, movie_add, MovieDelete

urlpatterns = [
    path('', MovieList.as_view(), name='home'),
    path('search/', movie_search, name='movie-search'),
    path('movie-add/<str:imdb_id>', movie_add, name='movie-add'),
    path('movie-delete/<int:pk>', MovieDelete.as_view(), name="movie-delete"),
]
