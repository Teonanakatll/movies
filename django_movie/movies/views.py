from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from . models import Movie


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # template_name = "movies/movies.html"


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    # Отвечает за поле по которому будет происходить поиск записи,
    # сравнивая с данными переданными из url
    slug_field = "url"
    # Шаблон неуказывается потому-что Джанго ищет шаблон по имени модели добавляя к нему "_detail"
    # Можно указать явно через template_name
