from django.contrib import admin

from .models import Board, UserResponse, OneTimeCode


class BoardAdmin(admin.ModelAdmin):
    list_display = ('author', 'title', 'description', 'category', 'upload')
    model = Board


admin.site.register(Board)


class UserResponseAdmin(admin.ModelAdmin):
    list_display = ('author', 'text', 'board', 'status')


admin.site.register(UserResponse)


class OneTimeCodeAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'used')


admin.site.register(OneTimeCode)
