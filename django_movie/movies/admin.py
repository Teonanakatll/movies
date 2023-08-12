from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)


# Класс для отображения в админке фильма связанных с ним коментариев
# class ReviewsInline(admin.StackedInline):

# Для отображения полей связанных коментариев в 1 строку (горизонтально)

class MovieShotsInline(admin.TabularInline):
    """ inline-форма добавления связанной (ForeignKey) записи в БД. """
    model = MovieShots
    # Кол-во inline-форм в админ-панели для модели.
    extra = 0


class ReviewsInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft")
    list_filter = ("category", "year")
    # Указываем по какому полю в связанной модели производить поиск
    search_fields = ("title", "category__name")
    list_editable = ("draft",)
    # В списке указываем классы которые мы хотим прикрепить, работает со связями ManyToMany и ForeignKey.
    inlines = [ReviewsInline, MovieShotsInline]
    # Отобразить панель редактирования сверху
    save_on_top = True
    # Сохранить как новый обьект
    save_as = True
    # Группировка полей в 1 строку (выводит только указанные поля)
    # fields = (("actors", "directors", "genres"),)

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'url': ('title',)}


    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), ),

        }),
        (None, {
            "fields": (("description", "poster"), )
        }),
        (None, {
            "fields": (("year", "world_premiere", "country"), )
        }),
        ("Actors", {
            "classes": ("collapse",),  # Классы в админке будут свёрнуты
            "fields": (("actors", "directors", "genres", "category"), )
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"), )
        }),
        ("Options", {
            "fields": (("url", "draft"), )
        }),
    )

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Режиссёры и Актёры"""
    list_display = ("name", "age")


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip")


@admin.register(MovieShots)
class MovieShots(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_html_photo")
    readonly_fields = ("get_html_photo",)

    # Метод для отображения миниатюр в админ панели, возвращает html-код
    # Параметр object ссылается на текущую запись списка (обьект модели Women)
    # Обращаемся к полю photo и берем url
    def get_html_photo(self, object):
        if object.image:  # Если фото существует
            # Функция mark_safe указывает не экранировать символы
            return mark_safe(f"<img src='{object.image.url}' width=250")

    # Меняем имя фото в админ панели
    get_html_photo.short_description = "Миниатюра"


admin.site.register(RatingStar)
