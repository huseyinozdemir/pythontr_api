from django.urls import path, include
from rest_framework.routers import DefaultRouter

from recipe import views

# /api/recipe/categories/1/
router = DefaultRouter()
router.register('categories', views.CategoryViewSet)
router.register('articles', views.ArticleViewSet)
router.register('comments', views.CommentViewSet)
router.register('messages', views.MessageViewSet)
app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls))
]
