from django.contrib import admin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):

    list_display = (
        'nickname',
        'username',
        'university',
        'date_joined',
    )

    list_display_links = (
        'nickname',
        'username',
    )
