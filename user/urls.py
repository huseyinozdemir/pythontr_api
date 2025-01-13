from django.urls import path, include

from user import views


app_name = 'user'

urlpatterns = [
     path('create/', views.CreateUserView.as_view(), name='create'),
     path('token/', views.CreateTokenView.as_view(), name='token'),
     path('me/', views.ManageUserView.as_view(), name='me'),
     path('admin/', include('user.admin.urls', namespace='admin'),
          name='admin'),
     path('activate/<uuid:code>/', views.ActivateUserView.as_view(),
          name='activate'),
     path('resend-activation/', views.ResendActivationView.as_view(),
          name='resend-activation'),
     path('reset-password/', views.PasswordResetView.as_view(),
          name='reset-password'),
     path('reset-password/confirm/', views.PasswordResetConfirmView.as_view(),
          name='reset-password-confirm'),
     path('reset-password/confirm/<str:uidb64>/<str:token>/',
          views.PasswordResetConfirmView.as_view(),
          name='reset-password-confirm'),
]
