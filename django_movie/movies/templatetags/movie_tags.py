from django import template
from movies.models import Category, Movie

register = template.Library()

# Оборачиваем функцию в декоратор, который зарегистрирует её как template-тег.
# После объявления тега необходимо перезапустить сервер, чтобы не было ошибки.
@register.simple_tag()
def get_categories():
    """ Вывод всех категорий. """
    return Category.objects.all()

# inclusion_tag - может рендерить шаблоны переданные в него
@register.inclusion_tag('tags/last_movies.html')
# В переменной count передаём количество выводимых фильмов (по умолчанию 5)
def get_last_movies(count=5):
    # Переменной movie присваиваем срез сортированный по id от начала до зночения переданного в count
    movies = Movie.objects.order_by("id")[:count]
    return {"last_movies": movies}

