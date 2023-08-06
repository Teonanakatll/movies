from django.urls import path

from . import views


urlpatterns = [
    # name для вставки в html {% url 'movie_detail' %}
    path("", views.MoviesView.as_view(), name='movies'),
    path("<slug:slug>/", views.MovieDetailView.as_view(), name="movie_detail")
]
