from django.contrib import admin
from .models import Author, News, Comment, CategoryNews, Subscription


# admin.site.unregister(Author) # разрегистрируем наши товары(пропадёт в админ панеле)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('authorUser', 'ratingAuthor',)
    list_filter = ('authorUser', 'ratingAuthor')
    search_fields = ('authorUser', 'ratingAuthor')
    model = Author


admin.site.register(Author)


# создаём новый класс для представления новостей в админке
class NewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'categoryType', 'date')
    list_filter = ('name', 'author', 'categoryType', 'date')  # добавляем примитивные фильтры в нашу админку
    search_fields = ('name', 'category__name')  # тут всё очень похоже на фильтры из запросов в базу
    model = News


admin.site.register(News, NewsAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('commentPost', 'commentUser', 'text', 'dateCreation', 'rating')
    list_filter = ('commentPost', 'commentUser', 'text', 'dateCreation', 'rating')
    search_fields = ('commentPost', 'commentUser', 'text', 'dateCreation', 'rating')
    model = Comment


admin.site.register(Comment, CommentAdmin)


class CategoryNewsAdmin(admin.ModelAdmin):
    # list_display = ('name', 'subscribers')
    list_filter = ('name', 'subscribers')
    search_fields = ('name',)
    model = CategoryNews


admin.site.register(CategoryNews, CategoryNewsAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('user', 'category')
    search_fields = ('name',)
    model = Subscription


admin.site.register(Subscription, SubscriptionAdmin)
