from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin

from .models import User
from .forms import UserCreationForm, UserChangeForm


class MyUserAdmin(UserAdmin, admin.ModelAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        'id',
        'last_login',
        'first_name',
        'last_name',
        'username',
        'email',
        'is_admin',
        'is_active',
    )
    list_filter = (
        'last_login',
        'is_admin',
        'is_active',
    )

    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Personal info', {'fields': (
            'first_name', 'last_name', 'phone',)}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2',)}),
        ('Personal Info', {'fields': (
            'first_name', 'last_name', 'phone',
        )}),
        ('Permissions', {'fields': ('is_active', 'is_admin',)})
    )
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, MyUserAdmin)
admin.site.unregister(Group)