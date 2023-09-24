# from django import forms
# from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User

#Кастомизируем форму регистрации SignupForm, которую предоставляет пакет allauth. Для этого используем приложение,
# в котором писали свою форму регистрации.
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives
from django.core.mail import mail_managers
from django.core.mail import mail_admins



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
#-----------------------------------------------
        # Убираем код добавления пользователя в группу при регистрации
        # common_users = Group.objects.get(name="common users")
        # user.groups.add(common_users)
#-----------------------------------------------
        # Добавляем код на отправку письма на email новому пользователю при регистрации
        # Функция send_mail позволяет отправить письмо указанному получателю в recipient_list.
        # send_mail(
        #     subject='Добро пожаловать на наш Новостной портал', # тема письма
        #     message=f'{user.username}, вы успешно зарегистрировались!', # сообщение
        #     from_email=None, # будет использовано значение DEFAULT_FROM_EMAIL которое мы указали в settings.py. Значение в письме от кого
        #     recipient_list=[user.email], # список получателей
        # )
        # return user
        subject = 'Добро пожаловать на наш новостной портал!'
        text = f'{user.username}, вы успешно зарегистрировались на сайте!'
        html = (
            f'<b>{user.username}</b>, вы успешно зарегистрировались на '
            f'<a href="http://127.0.0.1:8000/news">сайте</a>!'
        )
        msg = EmailMultiAlternatives(
            subject=subject, body=text, from_email=None, to=[user.email]
        )
        msg.attach_alternative(html, "text/html")
        msg.send()

# После чего в форме мы отправим им сообщение с помощью функции mail_managers:

        mail_managers(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        mail_admins(
            subject='Новый пользователь!',
            message=f'Пользователь {user.username} зарегистрировался на сайте.'
        )

        return user