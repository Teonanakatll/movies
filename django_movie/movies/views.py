from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from . models import Movie
from . forms import ReviewForm


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


class AddReview(View):
    """Отзывы"""
    def post(self, request, pk):
        # В созданную форму передаём данные из post запроса
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            # Так как отзыв мы привязываем к опред-ому фильму, необходимо указать к какому фильму будет привязан отзыв

            # Вызывая у формы метод save и передавая commit=False, приостанавливаем сохранение фармы, чтобы внести изменения
            form = form.save(commit=False)
            # Если в пост запроссе есть ключь "parent", тоесть если отроботал скрипт ответа на коментарий и в поле
            # "parent" подставлено значение
            if request.POST.get("parent", None):
                # Полю формы parent_id присваиваем числовое значение поля parent
                form.parent_id = int(request.POST.get("parent"))

            # В поле movie_id передаём pk из запроса (ForeignKey), чтобы при сохранении формы
            # создать запись Reviews в бд и привязать её к фильму
            # form.movie_id = pk

            form.movie = movie

            form.save()

        # Функция get_absolute_url() - вернёт шаблон movie_detail со слагом текущей модели movie
        return redirect(movie.get_absolute_url())
