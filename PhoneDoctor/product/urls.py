from django.urls import path

from . import views

urlpatterns = [
    path('new/', views.new, name ='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('brand/new/', views.newBrand,name='new_brand'),
    path('category/new/', views.newCategory,name='new_category')
]