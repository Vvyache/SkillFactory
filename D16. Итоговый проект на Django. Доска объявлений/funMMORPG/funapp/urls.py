from django.conf import settings  # Для загрузки файлов
from django.conf.urls.static import static  # Для загрузки файлов
from django.urls import path

from . import views
from .views import BoardList, BoardExtendedList, BoardCreate, BoardUpdate, register, user_login, user_logout, confirm_registration


urlpatterns = [
    path('', BoardList.as_view(), name='board'),
    path('<int:pk>', BoardExtendedList.as_view(), name='board_extended'),
    path('create/', BoardCreate.as_view(), name='board_create'),
    path('<int:pk>/edit/', BoardUpdate.as_view(), name='board_update'),
    path('register/', views.register, name='register'),  # URL для регистрации
    path('login/', user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # URL для выхода
    path('create_response/<int:board_id>/', views.create_user_response, name='create_response'),
    path('confirm-registration/', confirm_registration, name='confirm_registration'),
    path('user_responses/', views.user_responses, name='user_responses'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# if settings.DEBUG:
#     urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
