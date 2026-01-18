from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class MyUserAdmin(UserAdmin):
    # Добавляем наше поле confirmation_code в интерфейс админки
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('confirmation_code', 'bio')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('confirmation_code', 'bio')}),
    )