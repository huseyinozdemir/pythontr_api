from rest_framework.permissions import BasePermission

from core.models import Article


class IsAuthenticatedAndOwner(BasePermission):
    message = 'You must be the owner of this object.'

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        if hasattr(obj, 'user'):
            return obj.user == request.user
        else:
            return False


class IsAuthenticatedAndOwnerOld(BasePermission):

    def has_permission(self, request, view):
        try:
            result = True
            Article.objects.select_related('user').get(
                id=view.kwargs.get('id'),
                user_id=view.kwargs.get('user_id')
            )
        except Article.DoesNotExist:
            result = False
        if request.user.is_superuser:
            result = True
        return result
