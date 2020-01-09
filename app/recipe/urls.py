from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views


# /api/recipe/categories/1/
router = DefaultRouter()
router.register('categories', views.CategoryViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
