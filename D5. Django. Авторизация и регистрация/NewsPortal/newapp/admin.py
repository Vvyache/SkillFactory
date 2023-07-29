from django.contrib import admin
from .models import News, CategoryNews, Author


admin.site.register(CategoryNews)
admin.site.register(News)
admin.site.register(Author)
