from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category
from . forms import ReviewForm


class MoviesView(ListView):
    """Список фильмов"""
    model = Movie
    queryset = Movie.objects.filter(draft=False)
    # Шаблон не указывается потому-что Джанго ищет шаблон по имени модели добавляя к нему _list
    # template_name = "movies/movies.html"

    # # Для того чтобы на странице списка фильмов дополнительно вывести категории необходимо добавить метод
    # # get_context_data
    # def get_context_data(self, *args, **kwargs):
    #     # Вызываем метод super() родителя, таким образом мы получаем словарь и заносим его в реременную context
    #     context = super().get_context_data(*args, **kwargs)
    #     # Добавляем в него ключ 'categories' и заносим в него queryset всех наших категорий
    #     context['categories'] = Category.objects.all()
    #     return context


class MovieDetailView(DetailView):
    """Полное описание фильма"""
    model = Movie
    # Отвечает за поле по которому будет происходить поиск записи,
    # сравнивая с данными переданными из url
    slug_field = "url"
    # Шаблон неуказывается потому-что Джанго ищет шаблон по имени модели добавляя к нему "_detail"
    # Можно указать явно через template_name

    # # Для того чтобы на странице фильма дополнительно вывести категории необходимо добавить метод
    # # get_context_data
    # def get_context_data(self, *args, **kwargs):
    #     # Вызываем метод super() родителя, таким образом мы получаем словарь и заносим его в реременную context
    #     context = super().get_context_data(*args, **kwargs)
    #     # Добавляем в него ключ 'categories' и заносим в него queryset всех наших категорий
    #     context['categories'] = Category.objects.all()
    #     return context


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
