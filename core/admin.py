from django.contrib import admin
from django.contrib.contenttypes import admin as cadmin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _

from core import models


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    readonly_fields = ('created_at', 'slug')
    list_display = ('email', 'username', 'name', 'surname',
                    'created_at', 'updated_at',  'last_login')
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        (_('personel_info'), {'fields': ('username', 'name', 'surname',
                              'about_me', 'image',)}),
        (
            _('permissions'),
            {'fields': ('is_notification_email', 'is_staff', 'is_superuser',
                        'is_active', 'is_ban', 'is_delete',)}
        ),
        (
            _('important_dates'),
            {'fields': ('last_login', 'created_at',)}
        ),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


class CommentInline(cadmin.GenericTabularInline):
    model = models.Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'title', 'title_h1', 'is_active',
                    'is_delete')
    list_filter = ('id', 'title', 'title_h1')
    search_fields = ('id', 'title', 'title_h1')
    inlines = [
        CommentInline,
    ]


class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'content', 'content_object',
                    'is_active', 'is_delete',)
    list_filter = ('id', 'content')
    search_fields = ('id', 'content')
    inlines = [
        CommentInline,
    ]


class PageVisitAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'path', 'timestamp', 'ip_address',
                    'user_agent', 'referrer', 'method', 'device_type',
                    'language', 'ga_client_id', 'ga_session_id', 'gads_id',
                    'gpi_uid')
    list_filter = ('id', 'user', 'path', 'device_type', 'method', 'timestamp')
    search_fields = ('id', 'user', 'path')
    readonly_fields = ['timestamp']

    def has_add_permission(self, request):
        # Close add record
        return False


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category)
admin.site.register(models.Article, ArticleAdmin)
admin.site.register(models.Comment, CommentAdmin)
admin.site.register(models.Message)
admin.site.register(models.PageVisit, PageVisitAdmin)
