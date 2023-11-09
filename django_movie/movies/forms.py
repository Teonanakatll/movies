from django import forms

from .models import Reviews, RatingStar, Rating


# Если необходимо указывать в форме поля не связанные с моделями то наследуемся от forms
class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")


class RatingForm(forms.ModelForm):
    """Форма добавления рейтинга"""
    # Переопределяем поле star и с помощью ModelChoiceField передаём в него все экземпляры модели
    # RatingStar и виджет - радиокнопку (или можно выбрать выпадающий список или чекбокс)
    star = forms.ModelChoiceField(
        queryset=RatingStar.objects.all(), widget=forms.RadioSelect(), empty_label=None
    )

    class Meta:
        model = Rating
        fields = ("star",)

