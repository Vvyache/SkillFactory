# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

#Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth. Для этого используем приложение,
# в котором писали свою форму регистрации.
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group


# class SignUpForm(UserCreationForm):
#     email = forms.EmailField(label="Email")
#     first_name = forms.CharField(label="Имя")
#     last_name = forms.CharField(label="Фамилия")
#
#     class Meta:
#         model = User
#         fields = (
#             "username",
#             "first_name",
#             "last_name",
#             "email",
#             "password1",
#             "password2",
#         )

#Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth. Для этого используем приложение,
# в котором писали свою форму регистрации.


class CustomSignupForm(SignupForm):
    def save(self, request):
        user = super().save(request)
        common_users = Group.objects.get(name="common users")
        user.groups.add(common_users)
        return user