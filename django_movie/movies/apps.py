from django.apps import AppConfig


class MoviesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies'

    # Название приложения для админки
    verbose_name = "Фильмы"
