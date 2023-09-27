"""
Django settings for NewsPortal project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import logging
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-8os$jn610gu9qo9%h^gs8&=e@hp@t@#^m^6_5szg4f(zf_wv7j'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1']

# Application definition

INSTALLED_APPS = [
    'modeltranslation', # Модуль D14. Локализация и интернационализация. Переводим модели
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.flatpages',
    'newapp',
    'django_filters',
    'django_apscheduler',

    # В данный раздел добавьте 3 обязательных приложения allauth
    # и одно, которое отвечает за выход через Yandex
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.yandex',
]

# Ранее мы устанавливали значение для этой переменной,
# но всё равно убедитесь в её наличии.
SITE_ID = 1

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Пожалуй, один из главных промежуточных слоев, потому что он
    # реализует различные проверки безопасности — XSS, nosniff, HSTS, CORS, поддержка SSL и т. д.
    'django.contrib.sessions.middleware.SessionMiddleware',  # Включает механизм сессий в разрабатываемом приложении.
    'django.middleware.common.CommonMiddleware',  # Рекомендуемый для использования во всех Django-проектах, потому
    # что он позволяет выполнять стандартные процедуры над URL (приведение к единому шаблону с учетом слэшей и www в начале),
    # а также несколько других операций, рекомендуемых для всех приложений.
    'django.middleware.csrf.CsrfViewMiddleware', # Включает проверку безопасности от угроз типа CSRF.
    'django.contrib.auth.middleware.AuthenticationMiddleware', # Реализует основы аутентификации и идентификации.
    'django.contrib.messages.middleware.MessageMiddleware', # Включает поддержку сообщений, лежащих в основе работы с куки и сессиями.
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'newapp.middleware.MobileOrFullMiddleware',
    # Чтобы использовать полное кеширование всего проекта, добавляем:
    #     'django.middleware.cache.UpdateCacheMiddleware',
    #     'django.middleware.common.CommonMiddleware',
    #     'django.middleware.cache.FetchFromCacheMiddleware',
    'django.middleware.locale.LocaleMiddleware',# Промежуточный слой, позволяющий предоставлять контент в зависимости от настроек локализации, переданных в запросе. # Модуль D14. Локализация и интернационализация. Необходимо подключить LocaleMiddleware
]

ROOT_URLCONF = 'NewsPortal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

            ],
        },
    },
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

WSGI_APPLICATION = 'NewsPortal.wsgi.application'
LANGUAGES = [
    ('en-us', 'English'),
    ('ru', 'Русский')
]

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# ------------------------------------------------------------------------------------------------
# Настройка БД для работы с SQLite3
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# --------------------------------------------------------------------------------------------------
# Настройка БД для работы с PostgresSQL
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'postgres',
#         'USER': 'postgres',
#         'PASSWORD': '',
#         'HOST': 'localhost',
#         'PORT': '5432',
#     },
# }


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

# LANGUAGE_CODE = 'en-us'
LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATICFILES_DIRS = [BASE_DIR / 'static']

LOGIN_REDIRECT_URL = "/news"
LOGOUT_REDIRECT_URL = "/news"

# К специфичным для allauth переменным относятся те, что начинаются с ACCOUNT.

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'email'
# проверять почтовые ящики новых пользователей, в значении 'none' не проверяет
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_SUBJECT_PREFIX = '[News Portal ]'
# Указали форму для дополнительной обработки регистрации пользователя
ACCOUNT_FORMS = {"signup": "accounts.forms.CustomSignupForm"}

# Настройки почты
# Отправка писем на почту, но будьте внимательны. Тестировать такой код лучше с печатью писем в консоль.
# так как яндекс может заблокировать отправку на 24 часа, по причине подозрения на спам
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# Отправка писем в консоль
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = "arken27@yandex.ru"
EMAIL_HOST_PASSWORD = "pdnrfmzawiegyvzb"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_SUBJECT_PREFIX = '[News Portal] '
# адрес почты для отправки рассылки
DEFAULT_FROM_EMAIL = "arken27@yandex.ru"

SERVER_EMAIL = "arken27@yandex.ru"
MANAGERS = (
    ('Vyacheslav', 'arken27@yandex.ru'),
    # ('Petr', 'petr@yandex.ru'),
)
ADMINS = (
    ('Vyacheslav', 'arken27@yandex.ru'),
)

APSCHEDULER_DATETIME_FORMAT = 'N j, Y, f:s a'
APSCHEDULER_RUN_NOW_TIMEOUT = 25

SITE_URL = 'http://127.0.0.1:8000'

CELERY_BROKER_URL = 'redis://default:hIvD6bexDxzIpt3TZNWrxnffAR6YNxXI@redis-15637.c9.us-east-1-4.ec2.cloud.redislabs.com:15637'
CELERY_RESULT_BACKEND = 'redis://default:hIvD6bexDxzIpt3TZNWrxnffAR6YNxXI@redis-15637.c9.us-east-1-4.ec2.cloud.redislabs.com:15637'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

#  Добавляем кэширование через файловую систему в наш проект
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': os.path.join(BASE_DIR, 'cache_files'),
        # Указываем, куда будем сохранять кэшируемые файлы! Не забываем создать папку cache_files внутри папки с manage.py!
        'TIMEOUT': 60,
    }
}
# _______________________________________________________________________________________
# Модуль D13. Продвинутые возможности работы с Django

# Логирование

# Настройка логирования начинается с ключевого слова LOGGING
# 27.09 Пока отключил Логгирование по заданию
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'filters': {
#         'require_debug_true': {
#             '()': 'django.utils.log.RequireDebugTrue',
#         },
#         'require_debug_false': {
#             '()': 'django.utils.log.RequireDebugFalse',
#         },
#     },
#     'formatters': {
#         'verbose': {
#             'format': '{asctime} {levelname} {module} {message}',
#             'style': '{',
#         },
#         'simple': {
#             'format': '{asctime} {levelname} {message}',
#             'style': '{',
#         },
#         'error_critical': {
#             'format': '{asctime} {levelname} {message} {pathname} {exc_info}',
#             'style': '{',
#         },
#         'warning': {
#             'format': '{asctime} {levelname} {message} {pathname}',
#             'style': '{',
#         },
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'file_general': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'general.log',
#             'formatter': 'verbose',
#         },
#         'file_warning': {
#             'level': 'WARNING',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'warning',
#
#         },
#         'error_critical': {
#             'level': 'ERROR',
#             'filters': ['require_debug_true'],
#             'class': 'logging.StreamHandler',
#             'formatter': 'error_critical',
#
#         },
#         'file_errors': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'errors.log',
#             'formatter': 'error_critical',
#
#         },
#         'file_security': {
#             'level': 'INFO',
#             'filters': ['require_debug_false'],
#             'class': 'logging.FileHandler',
#             'filename': 'security.log',
#             'formatter': 'verbose',
#
#         },
#         'mail_admins': {
#             'level': 'ERROR',
#             'filters': ['require_debug_false'],
#             'class': 'django.utils.log.AdminEmailHandler',
#             'formatter': 'error_critical',
#
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['console', 'file_warning', 'error_critical', 'file_general'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#         'django.request': {
#             'handlers': ['mail_admins', 'file_errors'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.server': {
#             'handlers': ['mail_admins', 'file_errors'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.template': {
#             'handlers': ['file_errors'],
#             'level': 'ERROR',
#             'propagate': True,
#         },
#         'django.db.backends': {
#             'handlers': ['file_errors'],
#             'level': 'ERROR',
#             'propagate': True
#         },
#         'django.security': {
#             'handlers': ['file_security'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     }
# }

# Модуль D14. Локализация и интернационализация
# Добавляем настройки в строку:
LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale')
]
# Также необходимо подключить LocaleMiddleware в настройках Middleware:

