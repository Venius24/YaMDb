from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django import forms
from .models import User


class UserAdminForm(forms.ModelForm):
    role = forms.ChoiceField(
        choices=User.ROLE_CHOICES,
        widget=forms.Select,
        label='Роль'
    )
    
    class Meta:
        model = User
        fields = '__all__'


@admin.register(User)
class MyUserAdmin(UserAdmin):
    form = UserAdminForm
    
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Личная информация', {'fields': ('first_name', 'last_name', 'bio')}),
        ('Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Роль', {'fields': ('role',)}),
        ('Верификация', {'fields': ('confirmation_code',)}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'is_staff', 'is_superuser', 'role'),
        }),
    )
    
    list_display = ('username', 'email', 'role', 'is_staff', 'is_superuser', 'is_active')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'role', 'date_joined')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('-date_joined',)
