from django.urls import path, include
# Импортируем созданное нами представление
from .views import (NewsList, NewsDetail, NewsCreate,
                    NewsEdit, NewsDelete, NewsSearch, subscriptions
                    )
# from .views import IndexView
from django.views.decorators.cache import cache_page
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    # path — означает путь.
    # В данном случае путь ко всем товарам у нас останется пустым,
    # чуть позже станет ясно почему.
    # Т.к. наше объявленное представление является классом,
    # а Django ожидает функцию, нам надо представить этот класс в виде view.
    # Для этого вызываем метод as_view.

    # path('', cache_page(60)(NewsList.as_view()), name='news_list'), кэширование главной страницы на 60 секунд
    # path('<int:pk>', cache_page(60*5)(NewsDetail.as_view()), name='news_detail'), кэширование страниц с новостью на 300 секунд

    path('', NewsList.as_view(), name='news_list'),
    path('<int:pk>', NewsDetail.as_view(), name='news_detail'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:pk>/edit/', NewsEdit.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('subscriptions/', subscriptions, name='subscriptions'),
    # path('index/', IndexView.as_view()),  # !!!!!!!!!!!!!!!!!!!!
    path('i18n/', include('django.conf.urls.i18n')),
    # path('', include('basic.urls')),
]
