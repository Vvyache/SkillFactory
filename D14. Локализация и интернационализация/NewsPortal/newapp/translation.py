from .models import Author, News, Comment, CategoryNews, Subscription
from modeltranslation.translator import register, TranslationOptions


# регистрируем наши модели для перевода

@register(Author)
class AuthorTranslationOptions(TranslationOptions):
    fields = ('authorUser',)  # указываем, какие именно поля надо переводить в виде кортежа


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Comment)
class CommentTranslationOptions(TranslationOptions):
    fields = ('commentPost',)


@register(CategoryNews)
class CategoryNewsTranslationOptions(TranslationOptions):
    fields = ('name',)


@register(Subscription)
class SubscriptionTranslationOptions(TranslationOptions):
    fields = ('user',)
