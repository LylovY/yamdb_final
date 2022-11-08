from django.contrib import admin

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = (
        'username',
        'first_name',
        'last_name',
        'is_superuser',
        'email',
        'bio',
        'role',
        'code',
    )
    list_filter = (
        'is_superuser',
        'role',
    )
    search_fields = (
        'username',
        'email',
    )


admin.site.register(User, UserAdmin)
