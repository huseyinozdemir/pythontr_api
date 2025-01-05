from rest_framework.routers import DefaultRouter
from user.admin.views.view_user_admin import AdminUserViewSet
from user.admin.views.view_page_visit import PageVisitViewSet

app_name = 'admin'  # admin namespace için gerekli

router = DefaultRouter()
router.register('users', AdminUserViewSet, basename='users')
router.register('page-visits', PageVisitViewSet, basename='page-visits')

urlpatterns = router.urls
