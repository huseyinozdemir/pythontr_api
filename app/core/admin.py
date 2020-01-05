from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    readonly_fields = ('create_date',)
    list_display = ['email', 'username', 'name', 'surname',
                    'create_date', 'last_login']
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('Personel Info'), {'fields': ('username', 'name', 'surname',
                              'about_me', 'image',)}),
        (
            _('Permissions'),
            {'fields': ('is_notification_email', 'is_staff', 'is_superuser',
                        'is_active', 'is_ban', 'is_delete',)}
        ),
        (
            _('Important dates'),
            {'fields': ('last_login', 'create_date',)}
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
