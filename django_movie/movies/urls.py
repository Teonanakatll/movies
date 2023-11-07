from django.urls import path

from . import views


urlpatterns = [
    # name для вставки в html {% url 'movie_detail' %}
    path("", views.MoviesView.as_view(), name='movies'),
    # Размещён перед шаблоном поиском фильма по слагу чтобы не было ошибки с переменной queryset
    # url - для фильтра фильмов по году или жанру
    path("filter/", views.FilterMoviesView.as_view(), name='filter'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail"),
    path("review/<int:pk>/", views.AddReview.as_view(), name="add_review"),
    path("actor/<str:slug>/", views.ActorView.as_view(), name="actor_detail"),
]
