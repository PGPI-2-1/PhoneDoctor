from django.urls import path
from .views import RegistrationView
from custom_user.views import RegistrationView, MyLoginView
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', MyLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('dashboard/', views.dashboard , name='dashboard'),
]
