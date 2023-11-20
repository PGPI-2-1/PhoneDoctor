from django.urls import path

from django.contrib import admin
from custom_user.views import RegistrationView
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('admin', admin.site.urls),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
