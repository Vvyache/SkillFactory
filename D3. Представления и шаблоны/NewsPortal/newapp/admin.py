from django.contrib import admin
from .models import News, CategoryNews


admin.site.register(CategoryNews)
admin.site.register(News)
