from django import forms
from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Movie, MovieShots, Actor, Rating, RatingStar, Reviews

from ckeditor_uploader.widgets import CKEditorUploadingWidget



class MovieAdminForm(forms.ModelForm):
    # Добавляем виджет к полю класса
    description = forms.CharField(label='Описание',widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Категории"""
    list_display = ("id", "name", "url")
    list_display_links = ("name",)

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'url': ('name',)}


# Класс для отображения в админке фильма связанных с ним коментариев
# class ReviewsInline(admin.StackedInline):

# Для отображения полей связанных коментариев в 1 строку (горизонтально)
class ReviewsInline(admin.TabularInline):
    """Отзывы на странице фильма"""
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email")

class MovieShotsInline(admin.TabularInline):
    """Выводит кадры из фильма в админке фильма"""
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, object):
        if object.image:  # Если фото существует
            # Функция mark_safe указывает не экранировать символы
            return mark_safe(f"<img src='{object.image.url}' width=250")


        # Меняем имя фото в админ панели

    get_image.short_description = "Кадр из фильма"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """Фильмы"""
    list_display = ("title", "category", "url", "draft", "get_poster")
    list_filter = ("category", "year")

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'url': ('title',)}

    # Указываем по какому полю в связанной модели производить поиск
    search_fields = ("title", "category__name")
    # Поле доступное для редактирования
    list_editable = ("draft",)

    #Мои actions
    actions = ["publish", "unpublish"]

    # Добавляем форму ckeditor
    form = MovieAdminForm
    # В списке указываем классы которые мы хотим прикрепить, работает со связями ManyToMany и ForeignKey.
    inlines = [MovieShotsInline, ReviewsInline]
    # Отобразить панель редактирования сверху
    save_on_top = True
    # Сохранить как новый обьект
    save_as = True
    # Группировка полей в 1 строку (выводит только указанные поля)
    # fields = (("actors", "directors", "genres"),)

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'url': ('title',)}

    # Чтобы вывести изображение при просмотре записи
    readonly_fields = ("get_poster",)


    fieldsets = (
        (None, {
            "fields": (("title", "tagline"), )

        }),
        (None, {
            "fields": (("description", "poster", "get_poster"), ),
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

    def get_poster(self, object):
        if object.poster:
            return mark_safe(f"<img src='{object.poster.url}' height=350")

    get_poster.short_description = "Постер фильма"

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записи были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей было обновлено"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permission = ('change',)

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permission = ('change',)

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    """Отзывы"""
    list_display = ("name", "email", "parent", "movie", "id")
    readonly_fields = ("name", "email")


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Жанры"""
    list_display = ("name", "url")

    # Автоматически заполняет поле slug при добавлении экземпляра класса
    prepopulated_fields = {'url': ('name',)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    """Режиссёры и Актёры"""
    list_display = ("name", "age", "get_actor_image")
    # Чтобы вывести изображение при просмотре записи
    readonly_fields = ("get_actor_image",)

    def get_actor_image(self, object):
        if object.image:
            return mark_safe(f"<img src='{object.image.url}' width=250 ")

    get_actor_image.short_description = "Фото актёра"


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Рейтинг"""
    list_display = ("movie", "ip")


@admin.register(MovieShots)
class MovieShots(admin.ModelAdmin):
    """Кадры из фильма"""
    list_display = ("title", "movie", "get_html_photo")
    # Чтобы вывести изображение при просмотре записи
    readonly_fields = ("get_html_photo",)

    # Метод для отображения миниатюр в админ панели, возвращает html-код
    # Параметр object ссылается на текущую запись списка (обьект модели Movie)
    # Обращаемся к полю photo и берем url
    def get_html_photo(self, object):
        if object.image:  # Если фото существует
            # Функция mark_safe указывает не экранировать символы
            return mark_safe(f"<img src='{object.image.url}' width=250")

    # Меняем имя фото в админ панели
    get_html_photo.short_description = "Кадр из фильма"


admin.site.register(RatingStar)

# Изменение названия админ панели и имени страницы
admin.site.site_title = "Django Movies"
admin.site.site_header = "Django Movies"
