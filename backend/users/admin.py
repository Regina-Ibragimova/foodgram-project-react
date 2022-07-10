from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from users.models import Follow

User = get_user_model()


class FollowAdmin(admin.ModelAdmin):
    list_display = ('user', 'author')
    search_fields = ('user',)
    list_filter = ('user', 'author')
    empty_value_display = '-пусто-'


class ReUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name')
    list_filter = ('email', 'username')
    empty_value_display = "-пусто-"


admin.site.unregister(User)

admin.site.register(User, ReUserAdmin)
admin.site.register(Follow, FollowAdmin)
