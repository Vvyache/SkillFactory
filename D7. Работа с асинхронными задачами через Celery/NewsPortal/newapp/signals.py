from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import news_created

#-----------------------------------------------------------------------------------------------------------
# D6. Работа с почтой и выполнение задач по расписанию

# Отправка уведомления через apscheduler

# Теперь перепишем код обработчика сигнала для
# отправки сообщений всем пользователям, подписавшимся
# на обновления в этой категории.


# @receiver(post_save, sender=News)
# def news_created(instance, created, **kwargs):
#     if not created:
#         return
#
#     emails = User.objects.filter(
#         subscriptions__category=instance.category
#     ).values_list('email', flat=True)
#
#     subject = f'Новая новость в категории {instance.category}'
#
#     text_content = (
#         f'Новость: {instance.name}\n'
#         # f'Цена: {instance.price}\n\n'
#         f'Ссылка на новость: http://127.0.0.1:8000{instance.get_absolute_url()}'
#     )
#     html_content = (
#         f'Новость: {instance.name}<br>'
#         # f'Цена: {instance.price}<br><br>'
#         f'<a href="http://127.0.0.1:8000{instance.get_absolute_url()}">'
#         f'Ссылка на новость</a>'
#     )
#     for email in emails:
#         msg = EmailMultiAlternatives(subject, text_content, None, [email])
#         msg.attach_alternative(html_content, "text/html")
#         msg.send()


@receiver(post_save, sender=News)
def notify_about_new_post(sender, instance, created, **kwargs):
    if created:
        news_created.delay(instance.pk)

