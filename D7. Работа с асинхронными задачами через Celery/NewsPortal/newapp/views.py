# D3.2. Знакомство с django.views
# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД

from datetime import datetime, timedelta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (ListView, DetailView, CreateView, UpdateView, DeleteView)
from .models import News
from .filters import NewsFilter
from .forms import NewsForm
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from .models import Subscription, CategoryNews
from django.http import HttpResponse
from django.views import View
# from .tasks import hello, printer    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


class NewsList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = News
    # Поле, которое будет использоваться для сортировки объектов
    ordering = '-date'
    # Указываем имя шаблона, в котором будут все инструкции о том,
    # как именно пользователю должны быть показаны наши объекты
    template_name = 'news.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'news'
    # Метод get_context_data позволяет нам изменить набор данных,
    # который будет передан в шаблон.
    paginate_by = 4 # вот так мы можем указать количество записей на странице

    # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        # Получаем обычный запрос
        queryset = super().get_queryset()
        # Используем наш класс фильтрации.
        # self.request.GET содержит объект QueryDict, который мы рассматривали
        # в этом юните ранее.
        # Сохраняем нашу фильтрацию в объекте класса,
        # чтобы потом добавить в контекст и использовать в шаблоне.
        self.filterset = NewsFilter(self.request.GET, queryset)
        # Возвращаем из функции отфильтрованный список новостей
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        # С помощью super() мы обращаемся к родительским классам
        # и вызываем у них метод get_context_data с теми же аргументами,
        # что и были переданы нам.
        # В ответе мы должны получить словарь.
        context = super().get_context_data(**kwargs)
            # К словарю добавим текущую дату в ключ 'time_now'.
            # context['time_now'] = datetime.utcnow()
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        # Добавим ещё одну пустую переменную,
        # чтобы на её примере рассмотреть работу ещё одного фильтра.
        context['next_news'] = None
        return context


class NewsDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельному товару
    model = News
    # Используем другой шаблон — product.html
    template_name = 'specificnews.html'
    # Название объекта, в котором будет выбранный пользователем продукт
    context_object_name = 'news'

# Добавляем новое представление для создания товаров.


class NewsCreate(PermissionRequiredMixin,CreateView):
    # настроим выдачу ошибки с 403 кодом, для не авторизированных пользователей,
    # которые будут заходить на страницу создания товара.
    # raise_exception = True
    permission_required = ('newapp.add_news')
    # Указываем нашу разработанную форму
    form_class = NewsForm
    # модель товаров
    model = News
    # и новый шаблон, в котором используется форма.
    template_name = 'news_create.html'

# Добавляем новое представление для редактирования новостей.


class NewsEdit(PermissionRequiredMixin, UpdateView):
    permission_required = ('newapp.change_news')
    form_class = NewsForm
    model = News
    template_name = 'news_edit.html'

# Добавляем новое представление для удаления новостей.


class NewsDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('newapp.delete_news')
    model = News
    template_name = 'news_delete.html'
    success_url = reverse_lazy('news_list')


class NewsSearch(ListView):
    model = News
    ordering = '-date'
    template_name = 'news_search.html'
    context_object_name = 'news'
    paginate_by = 4

 # Переопределяем функцию получения списка новостей
    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = NewsFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем в контекст объект фильтрации.
        context['filterset'] = self.filterset
        return context


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = CategoryNews.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = CategoryNews.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('name')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )


# class IndexView(View):
#     def get(self, request):
#         printer.apply_async([10],
#                             eta = datetime.now() + timedelta(seconds=5))
#         hello.delay()
#         return HttpResponse('Hello!')



