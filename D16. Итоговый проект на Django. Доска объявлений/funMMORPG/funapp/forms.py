from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User

from .models import Board, UserResponse


class BoardForm(forms.ModelForm):
    description = forms.CharField(min_length=20, label='Описание')

    class Meta:
        model = Board
        fields = [
            'author',
            'title',
            'description',
            'category',
            'image',
            'video',

            ]
        labels = {
            'author': 'Автор',
            'title': 'Заголовок',
            'description': 'Описание',
            'category': 'Категория новости',
            'image': 'Картинка',
            'video': 'Видео'
            # 'upload': 'Загрузка файла',

        }

    def clean(self):
        cleaned_data = super().clean()
        text = cleaned_data.get("text")
        description = cleaned_data.get("description")

        if text == description:
            raise ValidationError(
                "Описание не должно быть идентично названию."
            )

        return cleaned_data


# Форма регистрации
class RegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password_confirm = forms.CharField(label='Подтвердите пароль', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=100, help_text='Required. Enter a valid email address.')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']  # Поля для регистрации

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')

        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают')

        return password_confirm


# Форма для входа
class LoginForm(forms.Form):
    username = forms.CharField(label='Имя пользователя')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)


# Форма для откликов
class UserResponseForm(forms.ModelForm):
    class Meta:
        model = UserResponse
        fields = ['text']


class ConfirmationForm(forms.Form):
    code = forms.CharField(max_length=6, required=True)


# Форма для откликов личной страницы
class FilterForm(forms.Form):
    ad_title = forms.CharField(label='Заголовок объявления', required=False)


# Форма для удаления откликов.
class DeleteForm(forms.Form):
    selected_responses = forms.ModelMultipleChoiceField(
        queryset=UserResponse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )


# AcceptForm - Форма для принятия откликов.
class AcceptForm(forms.Form):
    selected_responses = forms.ModelMultipleChoiceField(
        queryset=UserResponse.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
    )
