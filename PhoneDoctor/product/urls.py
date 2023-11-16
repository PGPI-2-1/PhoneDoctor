from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.new, name ='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
]