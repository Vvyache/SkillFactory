from django.conf import settings  # Для загрузки файлов
from django.conf.urls.static import static  # Для загрузки файлов
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
   path('admin/', admin.site.urls),
   path('pages/', include('django.contrib.flatpages.urls')),
   path('board/', include('funapp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
