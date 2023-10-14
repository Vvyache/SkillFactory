from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail

from .models import UserResponse


@receiver(pre_save, sender=UserResponse)
def my_handler(sender, instance, created, **kwargs):
    if instance.status: # Если автор объявления принял отклик, то ему приходит сообщение
        mail = instance.author.email
        send_mail(
            'Subject here',
            'Here is the message.',
            'host@mail.ru',
            [mail],
            fail_silently=False
        )
    mail = instance.board.author.email # Если просто появился отклик
    send_mail(
        'Subject here',
        'Here is the message.',
        'host@mail.ru',
        [mail],
        fail_silently=False
    )
