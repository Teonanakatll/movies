from django import forms

from . models import Reviews

# Если необходимо указывать в форме поля не связанные с моделями то наследуемся от forms
class ReviewForm(forms.ModelForm):
    """Форма отзывов"""
    class Meta:
        model = Reviews
        fields = ("name", "email", "text")

