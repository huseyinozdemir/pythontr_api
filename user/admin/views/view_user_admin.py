from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model

from user.admin import serializers


class AdminUserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.AdminUserListSerializer
    permission_classes = [IsAdminUser]
    queryset = get_user_model().objects.all().order_by('-created_at')
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['email', 'name', 'surname']
    filterset_fields = ['is_active', 'is_staff', "is_ban"]
    http_method_names = ['get', 'patch', 'delete']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.AdminUserDetailSerializer
        if self.action in ['update', 'partial_update']:
            return serializers.AdminUserActionSerializer
        return self.serializer_class

    def get_object(self):
        id = self.kwargs.get('pk')
        User = get_user_model()
        return User.objects.get(pk=id)

    def destroy(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "You cannot delete your own account"},
                status=status.HTTP_400_BAD_REQUEST
            )
        user.is_delete = True
        user.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, *args, **kwargs):
        user = self.get_object()
        if user == request.user:
            return Response(
                {"detail": "You cannot modify your own account"},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().partial_update(request, *args, **kwargs)
