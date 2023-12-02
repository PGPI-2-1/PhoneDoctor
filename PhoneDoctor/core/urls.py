from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:category>/', views.index, name='index_category'),
    path('brand/<str:brand>/', views.index, name='index_brand'),
    path('about-us/',views.about_us,name = 'about_us')
]
