from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# Модель доски объявления
class Board(models.Model):
    TYPE = (
        ('tanks', 'Танки'),
        ('heal', 'Хилы'),
        ('DD', 'ДД'),
        ('tradespeople', 'Торговцы'),
        ('guildmasters', 'Гильдмастеры'),
        ('questgivers', 'Квестгиверы'),
        ('blacksmiths', 'Кузнецы'),
        ('tanners', 'Кожевники'),
        ('potionmakers', 'Зельевары'),
        ('spellmasters', 'Мастера заклинаний'),
    )
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=64)
    description = models.TextField()
    category = models.CharField(max_length=32, choices=TYPE, default='tanks')
    date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='board_images/', blank=True, null=True)
    video = models.FileField(upload_to='board_videos/', blank=True, null=True)

    def __str__(self):
        return self.title.title()

    def get_absolute_url(self):
        return reverse('board_extended', args=[str(self.id)])


# Модель отклика на доску объявления
class UserResponse(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.text.title()

    def __str__(self):
        return f'Response by {self.author.username} to board #{self.board.id}'


class OneTimeCode(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)  # 6-значный код
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True)  # Дата истечения срока действия кода
    used = models.BooleanField(default=False)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_code = models.CharField(max_length=6)
    is_active = models.BooleanField(default=False)
