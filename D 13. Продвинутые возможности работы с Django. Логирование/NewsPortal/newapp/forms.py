from django import forms
from django.core.exceptions import ValidationError
from .models import News


class NewsForm(forms.ModelForm):
    description = forms.CharField(min_length=20, label='Описание')

    class Meta:
        model = News
        fields = [
            'author',
            'name',
            'description',
            'category',
            'categoryType'
            ]
        labels = {
            'author': 'Автор',
            'name': 'Заголовок',
            'description': 'Описание',
            'category': 'Категория новости',
            'categoryType': 'Тип'
        }

    def clean(self):
        cleaned_data = super().clean()
        name = cleaned_data.get("name")
        description = cleaned_data.get("description")

        if name == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data