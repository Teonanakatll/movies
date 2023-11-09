from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, Actor, Genre, Rating
from . forms import ReviewForm, RatingForm


class GenreYears:
    """ Жанры и года"""

    def get_genres(self):
        return Genre.objects.all()

    def get_years(self):
        # Функция values возвращает указанные словари, values_list кортежи
        return Movie.objects.filter(draft=False).values("year")


class MoviesView(GenreYears, ListView):
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


class MovieDetailView( GenreYears, DetailView):
    """Полное описание фильма"""
    model = Movie
    # Отвечает за поле по которому будет происходить поиск записи,
    # сравнивая с данными переданными из url
    slug_field = "url"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["star_form"] = RatingForm()
        return context
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


class ActorView(GenreYears, DetailView):
    """ Вывод информации о актёре. """
    model = Actor
    template_name = "movies/actor.html"
    # Поле по которому мы будем искать актёров
    slug_field = "name"


class FilterMoviesView(GenreYears, ListView):
    """Фильтр фильмов"""
    def get_queryset(self):
        # getlist - выбрать все зночения атрибута
        queryset = Movie.objects.filter(Q(year__in=self.request.GET.getlist("year")) |
                                        Q(genres__in=self.request.GET.getlist("genre")))
        return queryset


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")  # Метод disctinсt выбирает уникальные значения
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""


    def get_client_ip(self, request):
        # HTTP_X_FORWARDED_FOR — содержит цепочку прокси адресов и последним идёт IP
        # непосредственного клиента обратившегося к прокси серверу
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip

    def post(self, request):
        # Когда приходит пост запрос, передаём в форму запрас
        form = RatingForm(request.POST)

        if form.is_valid():
            # Проверяем экземпляры классов Rating по полям: ip, movie_id. И обновляем (поле defaults)
            # те привяжемся к другой звезде, или создаём новую запись RatingStar.
            Rating.objects.update_or_create(
                ip=self.get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


