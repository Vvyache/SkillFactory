import random
import string

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, PermissionDenied
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Board, User, UserResponse, OneTimeCode, UserProfile
from .forms import BoardForm, ConfirmationForm, RegistrationForm, LoginForm, UserResponseForm, FilterForm, DeleteForm, AcceptForm
from django.shortcuts import render, redirect


class BoardList(ListView):
    model = Board
    template_name = 'board.html'
    context_object_name = 'board'

    models = Board.objects.all()

    context = {
        'models': models,
    }


class BoardExtendedList(DetailView):
    model = Board
    template_name = 'board_extended.html'
    context_object_name = 'board'
    models = Board.objects.all()

    context = {
        'models': models,
    }


class BoardCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('funapp.add_board')
    form_class = BoardForm
    model = Board
    template_name = 'board_create.html'
    models = Board.objects.all()
    context = {
        'models': models,
    }


class BoardUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('funapp.board_update',)
    form_class = BoardForm
    model = Board
    template_name = 'board_update.html'

    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            raise PermissionDenied  # Вызываем ошибку 403
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Создать пользователя
            user = User.objects.create_user(username=username, email=email, password=password)

            # Генерация кода подтверждения
            code = ''.join(random.choices(string.digits, k=6))  # 6-значный код

            # Создать и связать экземпляр UserProfile с пользователем
            user_profile = UserProfile(user=user, activation_code=code)
            user_profile.save()

            # Отправка кода подтверждения на email пользователя
            subject = 'Подтверждение регистрации'
            message = f'Ваш код подтверждения: {code}'
            from_email = 'noreply@example.com'
            recipient_list = [email]
            send_mail(subject, message, from_email, recipient_list, fail_silently=False)
            return redirect('confirm_registration')  # Перенаправление на страницу подтверждения
    else:
        form = RegistrationForm()
    return render(request, 'registration/register.html', {'form': form})


# Вход пользователя с проверкой одноразового кода:
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('board')  # Перенаправление на главную страницу после входа
            else:
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'Неправильные учетные данные'})

    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})


# Выход пользователя
def user_logout(request):
    logout(request)
    return redirect('login')  # Перенаправление на страницу входа после выхода


# Представление для отправки откликов
@login_required
@permission_required('funapp.add_board', raise_exception=True)
def create_user_response(request, board_id):
    board = Board.objects.get(pk=board_id)

    if request.method == 'POST':
        form = UserResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.author = request.user
            response.board = board
            response.save()

            # Отправка уведомления на email объявителю о новом отклике
            send_notification_email(board.author.email, "Новый отклик на ваше объявление")

            # Отправка уведомления на email автору отклика о принятии отклика
            send_response_accepted_notification(request.user.email, "Ваш отклик был принят")

            return redirect('board_extended', board_id)
    else:
        form = UserResponseForm()
    return render(request, 'create_response.html', {'form': form, 'board': board})


def send_notification_email(to_email, subject):
    message = 'У вас новый отклик на объявление.'
    from_email = 'noreply@example.com'
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


def send_response_accepted_notification(to_email, subject):
    message = 'Ваш отклик был принят.'
    from_email = 'noreply@example.com'
    recipient_list = [to_email]

    send_mail(subject, message, from_email, recipient_list, fail_silently=False)


# Подтверждение регистрации
def confirm_registration(request):
    if request.method == 'POST':
        form = ConfirmationForm(request.POST)
        if form.is_valid():
            # Получить код подтверждения из формы
            code = form.cleaned_data['code']

            # Проверить, существует ли пользователь с таким кодом подтверждения
            try:
                user_profile = UserProfile.objects.get(activation_code=code)
                user_profile.user.is_active = True  # Активировать пользователя
                user_profile.user.save()
                user_profile.delete()  # Удалить экземпляр UserProfile после подтверждения
                return redirect('login')  # Перенаправить на страницу входа
            except UserProfile.DoesNotExist:
                form.add_error('code', 'Неправильный код подтверждения')

    else:
        form = ConfirmationForm()

    return render(request, 'registration/confirm_registration.html', {'form': form})


# Создание своей страницы с откликами
@login_required
@permission_required('funapp.add_board', raise_exception=True)
def user_responses(request):
    user_responses = UserResponse.objects.filter(author=request.user)
    filter_form = FilterForm()
    delete_form = DeleteForm()
    accept_form = AcceptForm()

    if request.method == 'POST':
        if 'filter_button' in request.POST:
            filter_form = FilterForm(request.POST)
            if filter_form.is_valid():
                ad_title = filter_form.cleaned_data.get('ad_title')
                user_responses = user_responses.filter(board__title__icontains=ad_title)
        elif 'delete_button' in request.POST:
            delete_form = DeleteForm(request.POST)
            if delete_form.is_valid():
                selected_responses = delete_form.cleaned_data.get('selected_responses')
                for response in selected_responses:
                    response.delete()
        elif 'accept_button' in request.POST:
            accept_form = AcceptForm(request.POST)
            if accept_form.is_valid():
                selected_responses = accept_form.cleaned_data.get('selected_responses')
                for response in selected_responses:
                    response.status = True
                    response.save()

    context = {
        'user_responses': user_responses,
        'filter_form': filter_form,
        'delete_form': delete_form,
        'accept_form': accept_form,
    }
    return render(request, 'user_responses.html', context)


@receiver(post_save, sender=Board)
def send_announcement_email(sender, instance, **kwargs):
    subject = 'Новое объявление: ' + instance.title
    message = 'Появилось новое объявление:\n\n' + instance.description
    from_email = 'noreply@example.com'
    recipient_list = [user.email for user in User.objects.all()]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)
