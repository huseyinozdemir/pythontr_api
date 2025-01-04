from rest_framework.routers import DefaultRouter
from user.admin.views import AdminUserViewSet

app_name = 'admin'  # admin namespace için gerekli

router = DefaultRouter()
router.register('users', AdminUserViewSet, basename='users')

urlpatterns = router.urls
