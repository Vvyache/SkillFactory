from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum
from django.core.validators import MinValueValidator
from django.urls import reverse
from django.core.cache import cache


class Author(models.Model):
    authorUser = models.OneToOneField(User, on_delete=models.CASCADE)
    ratingAuthor = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.authorUser.username

    def update_rating(self):
        postRat = self.post_set.aggregate(postRating=Sum('rating'))
        pRat = 0
        pRat += postRat.get('postRating')

        commentRat = self.authorUser.comment_set.aggregate(commentRating=Sum('rating'))
        cRat = 0
        cRat += commentRat.get('commentRating')

        self.ratingAuthor = pRat * 3 + cRat
        self.save()


class News(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    name = models.CharField(
        max_length=500,
        unique=True,  # названия новостей не должны повторяться
    )
    NEWS = 'Новость'
    ARTICLE = 'Статья'
    CATEGORY_CHOICES = (
        (NEWS, 'Новость'),
        (ARTICLE, 'Статья'),
    )
    categoryType = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default=ARTICLE)
    description = models.TextField()

    # поле категории будет ссылаться на модель категории
    category = models.ForeignKey(
        to='CategoryNews',
        on_delete=models.CASCADE,
        related_name='news')  # все новости в категории будут доступны через поле news

    date = models.DateTimeField(auto_now_add=True)
    # rating = models.SmallIntegerField(default=0)

    def __str__(self):
        return f'{self.name.title()}: {self.description[:20]}'

    def get_absolute_url(self):
        # return reverse('news_detail', args=[str(self.id)])
        return f'/news/{self.id}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # сначала вызываем метод родителя, чтобы объект сохранился
        cache.delete(f'news-{self.pk}')  # затем удаляем его из кэша, чтобы сбросить его


    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating += 1
        self.save()

    def preview(self):
        return self.text[0:123] + '...'


class Comment(models.Model):
    commentPost = models.ForeignKey(News, on_delete=models.CASCADE)
    commentUser = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    dateCreation = models.DateTimeField(auto_now_add=True)
    rating = models.SmallIntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()


# Категория, к которой будет привязываться новость
class CategoryNews(models.Model):
    # названия категорий тоже не должны повторяться
    name = models.CharField(max_length=100, unique=True)
    # subscribers = models.ManyToManyField(User, through='Subscription')
    subscribers = models.ManyToManyField(User, blank=True, related_name='categories', through='Subscription')  # 28.08 Убрал Null=True !!!!!!!!!!!!
    # subscribers = models.ManyToManyField('self', through='Subscription', related_name='categories', blank=True) # 26.09 Добавил для корректного выполения миграций

    def __str__(self):
        return self.name.title()


class Subscription(models.Model):
    user = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )
    category = models.ForeignKey(
        to='CategoryNews',
        on_delete=models.CASCADE,
        related_name='subscriptions',
    )

    def __str__(self):
        return f'{self.category.name}'