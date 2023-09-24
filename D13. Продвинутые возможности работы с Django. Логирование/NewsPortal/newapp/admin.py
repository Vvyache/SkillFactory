from django.contrib import admin
from .models import News, CategoryNews, Author, Subscription
# admin.site.unregister(Author) # разрегистрируем наши товары(пропадёт в админ панеле)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor',)
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser', 'ratingAuthor')


admin.site.register(Author)


# создаём новый класс для представления новостей в админке
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'categoryType', 'date')
    list_filter = ('name', 'author', 'categoryType', 'date')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу


admin.site.register(News, NewsAdmin)


class CategoryNewsAdmin(admin.ModelAdmin):
    # list_display = ('name', 'subscribers')
    list_filter = ('name', 'subscribers')
    search_fields = ('name',)


admin.site.register(CategoryNews, CategoryNewsAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    search_fields = ('name',)


admin.site.register(Subscription, SubscriptionAdmin)
