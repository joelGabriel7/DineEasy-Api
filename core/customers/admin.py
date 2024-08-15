from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from core.customers.models import CustomerUser
from django.urls import reverse
from django.utils.html import format_html
from rest_framework.authtoken.models import Token


class CustomerUserAdmin(UserAdmin):
    list_display = ('username', 'get_full_name', 'email', 'phone', 'get_groups', 'is_staff', 'show_token')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
    ordering = ('username',)

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        (_('Preferences'), {'fields': ('preferences',)}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'phone', 'groups'),
        }),
    )

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip() or "-"

    get_full_name.short_description = 'Name'

    def get_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

    get_groups.short_description = 'Groups'

    def show_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0]
        return format_html('<span title="{}">{}</span>', token.key, token.key[:10] + '...')

    show_token.short_description = 'Access Token'

    def view_token(self, obj):
        token = Token.objects.get_or_create(user=obj)[0]
        return token.key

    def get_readonly_fields(self, request, obj=None):
        if obj:  # editing an existing object
            return self.readonly_fields + ('view_token',)
        return self.readonly_fields


admin.site.register(CustomerUser, CustomerUserAdmin)
