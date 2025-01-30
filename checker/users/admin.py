from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import WhitelistedUser, BlacListUser


@admin.register(WhitelistedUser)
class UserProfileAdmin(UserAdmin):
    list_display = ('username',
                    'telegramm_username',)
    search_fields = ('username', 'telegramm_username',)
    empty_value_display = '-empty-'


@admin.register(BlacListUser)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('telegram_id',)
    search_fields = ('telegram_id',)
    empty_value_display = '-empty-'