from celery import shared_task
from newapp.models import News, CategoryNews, User, Subscription
import time, datetime
from django.template.loader import render_to_string
from django.core.mail import mail_managers, EmailMultiAlternatives
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


#
# @shared_task
# def hello():
#     time.sleep(10)
#     print("Hello, world!")
#
#
# @shared_task
# def printer(N):
#     for i in range(N):
#         time.sleep(1)
#         print(i+1)


@shared_task
def weekly_notifications():
    # Получим текущую дату и дату неделю назад
    today = datetime.datetime.now()
    last_week = today - datetime.timedelta(days=7)

    # Получим все новости, которые были опубликованы за последнюю неделю
    news = News.objects.filter(date__gte=last_week)
    # print(f'{news = }')

    # Получим список категорий этих новостей
    categories = set(news.values_list('category__name', flat=True))
    # print(f'{categories = }')

    # Найдем подписчиков, которые подписаны на эти категории
    subscribers = set(CategoryNews.objects.filter(name__in=categories).values_list('subscribers__email', flat=True))
    # print(f'{subscribers = }')

    # Для каждого подписчика отправим письмо только с новостями из его категорий
    for subscriber in subscribers:
        categories_subscriber = set(
            CategoryNews.objects.filter(subscribers__email=subscriber).values_list('name', flat=True))
        news_subscriber = news.filter(category__name__in=categories_subscriber)

        # Создаем содержимое электронного письма на основе шаблона 'daily_post.html'
        html_content = render_to_string(
            'daily_post.html',
            {
                'Link': settings.SITE_URL,
                'news': news_subscriber,
            }
        )

        # Создаем электронное письмо
        msg = EmailMultiAlternatives(
            subject='Статьи за неделю',
            body='',
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[subscriber],
        )

        # Подключаем HTML версию письма
        msg.attach_alternative(html_content, 'text/html')

        # Отправляем письмо
        msg.send()


@shared_task
def news_created(pk):
    news = News.objects.get(pk=pk)
    name = news.name
    category = news.category
    subscribers_emails = []
    subscribers = Subscription.objects.filter(category=category)
    subscribers_emails += [subs.user.email for subs in subscribers]
    html_content = render_to_string(
        'post_created_email.html',
        {
            'text': f'{news.name}',
            'link': f'{settings.SITE_URL}/news/{pk}',
        }
    )
    msg = EmailMultiAlternatives(
        subject=name,
        body='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=subscribers_emails
    )
    msg.attach_alternative(html_content, "text/html")
    msg.send()