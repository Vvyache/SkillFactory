# В первую очередь мы импортируем библиотеку для взаимодействия
# с операционной системой и саму библиотеку Celery
import os
from celery import Celery
from celery.schedules import crontab

# Второй строчкой мы связываем настройки Django с настройками
# Celery через переменную окружения.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')

# Далее мы создаем экземпляр приложения Celery и устанавливаем
# для него файл конфигурации. Мы также указываем пространство имен,
# чтобы Celery сам находил все необходимые настройки в общем конфигурационном
# файле settings.py. Он их будет искать по шаблону «CELERY_***».
app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Последней строчкой мы указываем Celery автоматически искать задания в
# файлах tasks.py каждого приложения проекта.
app.autodiscover_tasks()

# app.conf.beat_schedule = {
#     'print_every_5_seconds': {
#         'task': 'board.tasks.printer',
#         'schedule': 5,
#         'args': (5,),
#     },
# }

app.conf.beat_schedule = {
    'action_every_monday_8_00_am': {
        'task': 'newapp.tasks.weekly_notifications',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'schedule': 120 # отправка каждые 120 секунд

    },
}
