from django.urls import path

from . import views
from product.views import product_info

urlpatterns = [
    path('new/', views.new, name ='new'),
    path('<int:pk>/delete/', views.delete, name='delete'),
    path('<int:pk>/edit/', views.edit, name='edit'),
    path('brand/new/', views.new_brand, name='new_brand'),
    path('category/new/', views.new_category, name='new_category'), 
    path('<int:pk>', product_info, name='product_info'),
    path('nueva_opinion/<int:product_id>/', views.nueva_opinion, name='nueva_opinion')
]